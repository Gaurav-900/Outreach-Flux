import os
import base64
from email.message import EmailMessage
import mimetypes

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    def __init__(self):
        self.credentials_path = os.getenv("GMAIL_CREDENTIALS_JSON_PATH", "config/credentials.json")
        self.token_path = os.getenv("GMAIL_TOKEN_JSON_PATH", "config/token.json")
        self.resume_path = os.getenv("RESUME_PATH", "config/resume.pdf")
        self.creds = None
        self._authenticate()

    def _authenticate(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"[GmailService] Failed to refresh token: {e}")
                    self.creds = None
            
            if not self.creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Credentials not found at {self.credentials_path}")
                
                # Perform OAuth flow. Note: This requires a browser interaction.
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                # We use run_local_server() which blocks until the user logs in.
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token_file:
                token_file.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def _verify_resume(self):
        if not os.path.exists(self.resume_path):
            raise FileNotFoundError(f"Configured resume file not found at {self.resume_path}")
        if not os.access(self.resume_path, os.R_OK):
            raise PermissionError(f"Cannot read resume file at {self.resume_path}")

    def send_email(self, to_email: str, subject: str, body_text: str, thread_id: str = None, in_reply_to_message_id: str = None) -> dict:
        """Sends an email via Gmail API and returns the sent message info containing id and threadId."""
        self._verify_resume()

        message = EmailMessage()
        message["To"] = to_email
        message["Subject"] = subject
        
        if in_reply_to_message_id:
            # We need to wrap it in brackets if it isn't already, but assuming we fetch the raw header or we just pass the raw ID
            # Let's safely format it
            msg_id_header = in_reply_to_message_id
            if not msg_id_header.startswith('<'):
                msg_id_header = f'<{msg_id_header}>'
            message["In-Reply-To"] = msg_id_header
            message["References"] = msg_id_header
            
        message.set_content(body_text)

        # Attach resume
        ctype, encoding = mimetypes.guess_type(self.resume_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        
        with open(self.resume_path, "rb") as fp:
            attachment_data = fp.read()
            
        message.add_attachment(
            attachment_data,
            maintype=maintype,
            subtype=subtype,
            filename=os.path.basename(self.resume_path)
        )

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        
        if thread_id:
            create_message["threadId"] = thread_id
        
        try:
            send_message = self.service.users().messages().send(userId="me", body=create_message).execute()
            print(f"[GmailService] Sent message to {to_email}. Message Id: {send_message['id']}")
            return send_message
        except Exception as error:
            print(f"[GmailService] An error occurred while sending email: {error}")
            raise error
