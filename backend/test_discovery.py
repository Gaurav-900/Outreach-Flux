import asyncio
from app.services.orchestrator import DiscoveryOrchestrator
async def main():
    orchestrator = DiscoveryOrchestrator()
    await orchestrator.run_discovery_for_profile(0) # Profile 0 is Backend / API
asyncio.run(main())
