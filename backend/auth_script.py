from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
credentials_path = 'config/credentials.json'
token_path = 'config/token.json'

if not os.path.exists(credentials_path):
    print("Error: config/credentials.json not found!")
    exit(1)

print("Starting Google Auth flow. Please check your browser...")
flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
creds = flow.run_local_server(port=0)

with open(token_path, 'w') as token_file:
    token_file.write(creds.to_json())

print("Successfully authenticated! config/token.json has been created.")
