import os.path
from datetime import datetime, timezone, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DocHandler:

    def __init__(self):
        self.creds = None
        self.validate()


    def validate(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file()
                creds = flow.run_local_server(port=0)


    def last_modified(self):
        pass

    def pull_doc(self):
        pass

    