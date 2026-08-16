import asyncio
from app.services.outreach_generator import OutreachGeneratorService
async def main():
    gen = OutreachGeneratorService()
    await gen.generate_batch()
asyncio.run(main())
