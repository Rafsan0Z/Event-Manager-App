from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from pathlib import Path
from Label import Label

import os

def EmailFactory():
    try:
        handler = EmailHandler()
    except Exception as e:
        print(e)
    else:
        return handler

class EmailHandler:

    def __init__(self):
        load_dotenv()
        self.creds = None
        self.SCOPES = [os.getenv("READ_ONLY_SCOPE")]
        self.validate()
        self.service = build("gmail", "v1", credentials=self.creds)

    def validate(self):
        authen_path = str(Path(__file__).parent) + os.getenv('AUTHENTIFICATION_PATH')
        token_path = str(Path(__file__).parent) + os.getenv('TOKEN_PATH')
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    authen_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

    def process_labels(self, labels):
        
        processed = {}

        for label in labels:
            name = label["name"]
            subname = None
            if '/' in name:
                name, subname = name.split('/')

            if name not in processed:
                processed[name] = Label(name)
            if subname:
                processed[name].add_sublabels(subname)
        
        return processed.values()

            
                

    def get_labels(self):
        results = self.service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        processed_labels = self.process_labels(labels)

        print("These are the following labels: ")
        for label in processed_labels:
            print(label)
    
