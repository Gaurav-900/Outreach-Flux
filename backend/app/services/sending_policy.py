import os
from datetime import datetime, timezone

from app.core.supabase import supabase
from app.services.gmail import GmailService

class SendingOrchestrator:
    def __init__(self):
        self.kill_switch = os.getenv("GLOBAL_KILL_SWITCH", "false").lower() == "true"
        self.auto_send = os.getenv("AUTO_SEND_ENABLED", "false").lower() == "true"
        
        try:
            self.daily_limit = int(os.getenv("DAILY_SEND_LIMIT", "20"))
        except ValueError:
            self.daily_limit = 20

        # Don't initialize GmailService in init because it might trigger OAuth blocking flow
        # We only initialize it if we actually need to send something.
        self.gmail = None

    def _get_gmail_service(self):
        if not self.gmail:
            self.gmail = GmailService()
        return self.gmail

    def _get_today_send_count(self) -> int:
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        res = supabase.table('outreach').select('id', count='exact').eq('status', 'SENT').gte('updated_at', today_start).execute()
        return res.count if res.count is not None else 0

    def process_queue(self):
        print("[SendingOrchestrator] Processing outreach queue...")
        
        if self.kill_switch:
            print("[SendingOrchestrator] GLOBAL_KILL_SWITCH is enabled. Aborting all sends.")
            return

        today_count = self._get_today_send_count()
        if today_count >= self.daily_limit:
            print(f"[SendingOrchestrator] Daily limit of {self.daily_limit} reached ({today_count} sent today). Aborting.")
            return

        # Fetch eligible drafts
        # Modes:
        # MANUAL: user manually updates status to 'APPROVED'
        # AUTO: drafts in 'QUEUED' are processed if AUTO_SEND_ENABLED is true.
        statuses_to_fetch = ['APPROVED']
        if self.auto_send:
            statuses_to_fetch.append('QUEUED')

        res = supabase.table('outreach').select('*, contacts(*)').in_('status', statuses_to_fetch).execute()
        drafts = res.data
        
        if not drafts:
            print("[SendingOrchestrator] No approved or queued drafts to send.")
            return

        available_capacity = self.daily_limit - today_count
        drafts_to_process = drafts[:available_capacity]
        
        if not drafts_to_process:
            return
            
        # Initialize Gmail (will raise if credentials.json is missing or if resume is missing)
        try:
            gmail_service = self._get_gmail_service()
            gmail_service._verify_resume() # Fail fast if resume is missing before attempting any sends
        except Exception as e:
            print(f"[SendingOrchestrator] Initialization failed: {e}")
            return

        for draft in drafts_to_process:
            draft_id = draft['id']
            contact = draft.get('contacts')
            
            if not contact or not contact.get('email'):
                self._mark_failed(draft_id, "No valid email address found in contact.")
                continue

            # Check verification rule: "only verified recipients may be sent to"
            # If it's an auto-send (QUEUED), enforce verification rigidly
            if draft['status'] == 'QUEUED' and contact.get('verification_status') != 'VALID':
                print(f"[SendingOrchestrator] Skipping auto-send for {draft_id}: Contact not verified.")
                continue

            # Update status to processing state to prevent duplicate parallel processing
            current_status = draft['status']
            new_status = 'AUTO_APPROVED' if current_status == 'QUEUED' else 'APPROVED'
            
            email = contact['email']
            subject = draft['subject']
            body = draft['body']
            
            print(f"[SendingOrchestrator] Sending email to {email} (Draft {draft_id})...")
            
            try:
                result = gmail_service.send_email(to_email=email, subject=subject, body_text=body)
                
                # Update DB with success
                supabase.table('outreach').update({
                    'status': 'SENT',
                    'gmail_message_id': result.get('id'),
                    'gmail_thread_id': result.get('threadId'),
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', draft_id).execute()
                print(f"[SendingOrchestrator] Successfully marked {draft_id} as SENT.")
                
            except Exception as e:
                print(f"[SendingOrchestrator] Failed to send email for draft {draft_id}: {e}")
                self._mark_failed(draft_id, str(e))

    def _mark_failed(self, draft_id: str, error: str):
        try:
            supabase.table('outreach').update({
                'status': 'FAILED',
                'error_message': error,
                'updated_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', draft_id).execute()
        except Exception as e:
            print(f"[SendingOrchestrator] Critical error updating failure state for {draft_id}: {e}")
