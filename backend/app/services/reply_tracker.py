import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.core.supabase import supabase

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

class ReplyTrackerService:
    def __init__(self):
        self.token_path = os.getenv("GMAIL_TOKEN_JSON_PATH", "config/token.json")
        self.creds = None
        self.service = None

    def _authenticate_silently(self) -> bool:
        if not os.path.exists(self.token_path):
            return False
        
        try:
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                with open(self.token_path, 'w') as token_file:
                    token_file.write(self.creds.to_json())
            
            if self.creds and self.creds.valid:
                self.service = build('gmail', 'v1', credentials=self.creds)
                return True
        except Exception as e:
            print(f"[ReplyTracker] Authentication error: {e}")
            
        return False

    def check_for_replies(self) -> Dict[str, Any]:
        """Polls Gmail for new replies on SENT outreaches and updates Supabase."""
        print("[ReplyTracker] Starting reply check...")
        
        if not self._authenticate_silently():
            return {"status": "error", "message": "Gmail is not authenticated. Please run sending orchestrator once to authenticate via browser."}

        # Fetch eligible outreaches
        res = supabase.table('outreach').select('id, gmail_thread_id, gmail_message_id, reply_status').eq('status', 'SENT').in_('reply_status', ['PENDING', 'AUTO_REPLY', 'UNKNOWN']).execute()
        outreaches = res.data

        if not outreaches:
            self._update_last_check()
            return {"status": "success", "message": "No pending outreaches to check.", "processed": 0, "new_replies": 0}

        new_replies_count = 0

        for outreach in outreaches:
            thread_id = outreach['gmail_thread_id']
            if not thread_id:
                continue

            try:
                # Fetch thread
                thread = self.service.users().threads().get(userId='me', id=thread_id).execute()
                messages = thread.get('messages', [])
                
                # We only care about messages that are NOT our original sent message (the very first one or ones we sent)
                for msg in messages:
                    msg_id = msg['id']
                    
                    # Skip if we sent it
                    if outreach['gmail_message_id'] == msg_id:
                        continue
                        
                    # Check if we already processed this reply
                    existing_reply = supabase.table('replies').select('id').eq('gmail_message_id', msg_id).execute()
                    if existing_reply.data:
                        continue # Already processed
                        
                    # Fetch headers to determine sender and classification
                    headers = msg.get('payload', {}).get('headers', [])
                    header_dict = {h['name'].lower(): h['value'] for h in headers}
                    
                    sender = header_dict.get('from', '')
                    # Simple check to skip if it's from us (in case we sent a follow up)
                    # We could strictly check email, but usually "from:me" filter or similar is better.
                    # If there's a label "SENT", it's from us.
                    if 'SENT' in msg.get('labelIds', []):
                        continue
                        
                    classification = self._classify_message(header_dict)
                    
                    snippet = msg.get('snippet', '')
                    
                    # Store reply
                    supabase.table('replies').insert({
                        'outreach_id': outreach['id'],
                        'gmail_message_id': msg_id,
                        'gmail_thread_id': thread_id,
                        'classification': classification,
                        'headers': header_dict,
                        'body_snippet': snippet
                    }).execute()
                    
                    new_replies_count += 1
                    
                    # Update outreach reply_status based on priority (HUMAN > AUTO > UNKNOWN > PENDING)
                    current_status = outreach['reply_status']
                    if classification == 'HUMAN_REPLY':
                        outreach['reply_status'] = 'HUMAN_REPLY'
                    elif classification == 'AUTO_REPLY' and current_status != 'HUMAN_REPLY':
                        outreach['reply_status'] = 'AUTO_REPLY'
                    elif classification == 'UNKNOWN' and current_status == 'PENDING':
                        outreach['reply_status'] = 'UNKNOWN'

                # Persist updated status
                supabase.table('outreach').update({
                    'reply_status': outreach['reply_status'],
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', outreach['id']).execute()

            except Exception as e:
                print(f"[ReplyTracker] Error processing thread {thread_id}: {e}")

        self._update_last_check()
        return {
            "status": "success", 
            "message": f"Successfully processed {len(outreaches)} outreaches.", 
            "processed": len(outreaches), 
            "new_replies": new_replies_count
        }

    def _classify_message(self, headers: Dict[str, str]) -> str:
        """Deterministic heuristic classifier for auto vs human replies."""
        # 1. Check auto-submitted headers
        auto_sub = headers.get('auto-submitted', '').lower()
        if auto_sub and auto_sub != 'no':
            return 'AUTO_REPLY'
            
        x_autoreply = headers.get('x-autoreply', '').lower()
        if x_autoreply == 'yes':
            return 'AUTO_REPLY'
            
        precedence = headers.get('precedence', '').lower()
        if precedence in ['bulk', 'auto_reply', 'list']:
            return 'AUTO_REPLY'
            
        # 2. Check subject patterns
        subject = headers.get('subject', '').lower()
        auto_patterns = [
            'out of office',
            'automatic reply',
            'delivery status notification',
            'undeliverable',
            'message not delivered'
        ]
        if any(pattern in subject for pattern in auto_patterns):
            return 'AUTO_REPLY'
            
        # If no strict auto-reply markers are found, assume it is a human reply (or at least warrants human attention)
        return 'HUMAN_REPLY'

    def _update_last_check(self):
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            supabase.table('app_state').upsert({
                'key': 'last_reply_check',
                'value': {'timestamp': timestamp}
            }).execute()
        except Exception:
            pass
