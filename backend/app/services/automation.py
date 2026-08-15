import os
from datetime import datetime, timezone, timedelta

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.services.orchestrator import DiscoveryOrchestrator
from app.services.outreach_generator import OutreachGeneratorService
from app.services.reply_tracker import ReplyTrackerService
from app.services.sending_policy import SendingOrchestrator
from app.services.gmail import GmailService

class AutomationOrchestrator:
    def __init__(self):
        self.discovery_orchestrator = DiscoveryOrchestrator()
        self.generator = OutreachGeneratorService()
        self.reply_tracker = ReplyTrackerService()
        self.sender = SendingOrchestrator()
        self.kill_switch = os.getenv("GLOBAL_KILL_SWITCH", "false").lower() == "true"
        self.gmail = None

    async def run_automation_tick(self):
        print("=== [AutomationOrchestrator] Starting Automation Tick ===")
        
        # 1. Profile Rotation and Discovery
        try:
            await self._run_discovery()
        except Exception as e:
            print(f"[AutomationOrchestrator] Discovery failed: {e}")

        # 2. Draft Generation
        try:
            print("[AutomationOrchestrator] Generating drafts for READY_FOR_OUTREACH opportunities...")
            # Generate up to 10 drafts per tick to respect limits
            await self.generator.generate_drafts(limit=10)
        except Exception as e:
            print(f"[AutomationOrchestrator] Draft generation failed: {e}")

        # 3. Reply Tracking
        try:
            print("[AutomationOrchestrator] Polling for new replies...")
            self.reply_tracker.check_for_replies()
        except Exception as e:
            print(f"[AutomationOrchestrator] Reply tracking failed: {e}")

        # 4. Follow Ups
        if not self.kill_switch:
            try:
                self._process_follow_ups()
            except Exception as e:
                print(f"[AutomationOrchestrator] Follow-ups failed: {e}")
        else:
            print("[AutomationOrchestrator] Kill switch enabled. Skipping follow-ups.")

        # 5. Sending
        if not self.kill_switch:
            try:
                print("[AutomationOrchestrator] Triggering sending queue (respects AUTO_SEND_ENABLED internally)...")
                self.sender.process_queue()
            except Exception as e:
                print(f"[AutomationOrchestrator] Sending failed: {e}")
        else:
            print("[AutomationOrchestrator] Kill switch enabled. Skipping sending.")

        print("=== [AutomationOrchestrator] Automation Tick Complete ===")

    async def _run_discovery(self):
        print('[AutomationOrchestrator] Starting discovery rotation tick...')
        candidate_config = get_candidate_profile()
        profiles_count = len(candidate_config.discovery_profiles)
        
        if profiles_count == 0:
            print('[AutomationOrchestrator] No discovery profiles found in candidate.json.')
            return

        state_res = supabase.table('discovery_state') \
            .select('*') \
            .order('updated_at', desc=True) \
            .limit(1) \
            .execute()
            
        state_data = state_res.data[0] if state_res.data else None
        
        next_index = 0
        state_id = None

        if state_data:
            state_id = state_data['id']
            last_index = state_data.get('last_profile_index', 0)
            next_index = (last_index + 1) % profiles_count

        await self.discovery_orchestrator.run_discovery_for_profile(next_index)

        now_iso = datetime.now(timezone.utc).isoformat()
        
        if state_id:
            supabase.table('discovery_state').update({
                'last_run_at': now_iso,
                'last_profile_index': next_index,
                'updated_at': now_iso
            }).eq('id', state_id).execute()
        else:
            supabase.table('discovery_state').insert({
                'last_run_at': now_iso,
                'last_profile_index': next_index
            }).execute()

    def _process_follow_ups(self):
        print("[AutomationOrchestrator] Checking for follow-up opportunities...")
        # A follow up is sent if:
        # - status is SENT
        # - reply_status is PENDING
        # - followed_up is FALSE
        # - updated_at (which is when it was SENT or last updated) is older than 3 days.
        
        threshold = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
        
        res = supabase.table('outreach') \
            .select('*, contacts(email)') \
            .eq('status', 'SENT') \
            .eq('reply_status', 'PENDING') \
            .eq('followed_up', False) \
            .lt('updated_at', threshold) \
            .execute()
            
        drafts = res.data
        if not drafts:
            print("[AutomationOrchestrator] No follow-ups needed at this time.")
            return
            
        print(f"[AutomationOrchestrator] Found {len(drafts)} outreaches needing follow up.")
        
        # Get Gmail service
        if not self.gmail:
            self.gmail = GmailService()
            
        # Follow up template
        follow_up_body = (
            "Hi,\n\n"
            "I'm just following up on my previous email. I'm very interested in the opportunity "
            "and would love to connect if you have a moment.\n\n"
            "Best,\n"
        )
            
        for draft in drafts:
            contact = draft.get('contacts')
            if not contact or not contact.get('email'):
                continue
                
            email = contact['email']
            thread_id = draft.get('gmail_thread_id')
            msg_id = draft.get('gmail_message_id')
            
            if not thread_id or not msg_id:
                continue
                
            print(f"[AutomationOrchestrator] Sending follow-up to {email} (Draft {draft['id']})")
            
            try:
                # Add "Re: " to subject if not present
                subject = draft.get('subject', 'Following up')
                if not subject.lower().startswith("re:"):
                    subject = f"Re: {subject}"
                    
                self.gmail.send_email(
                    to_email=email,
                    subject=subject,
                    body_text=follow_up_body,
                    thread_id=thread_id,
                    in_reply_to_message_id=msg_id
                )
                
                supabase.table('outreach').update({
                    'followed_up': True,
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', draft['id']).execute()
                
            except Exception as e:
                print(f"[AutomationOrchestrator] Failed to send follow-up for {draft['id']}: {e}")
