from app.services.sending_policy import SendingOrchestrator
import asyncio

def main():
    sender = SendingOrchestrator()
    sender.process_queue()

if __name__ == "__main__":
    main()
