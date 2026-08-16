import asyncio
from app.services.outreach_generator import OutreachGeneratorService
from app.services.sending_policy import SendingOrchestrator
from app.core.supabase import supabase

async def main():
    print("Generating...")
    generator = OutreachGeneratorService()
    await generator.generate_batch()
    
    print("Approving drafts...")
    supabase.table('outreach').update({'status': 'APPROVED'}).eq('status', 'DRAFT').execute()
    
    print("Sending...")
    sender = SendingOrchestrator()
    sender.process_queue()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
