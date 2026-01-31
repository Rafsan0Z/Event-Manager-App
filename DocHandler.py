import os.path
import os
import json
from datetime import datetime, timezone, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from pathlib import Path

class DocHandler:

    def __init__(self):
        load_dotenv()
        self.creds = None
        self.validate()


    def validate(self):
        self.SCOPES = [os.getenv('DRIVE_SCOPE'), os.getenv('DOC_SCOPE')]
        authen_path = str(Path(__file__).parent) + os.getenv('AUTHENTIFICATION_PATH')
        token_path = str(Path(__file__).parent) + os.getenv('TOKEN_PATH')
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(authen_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())



    def last_modified(self):
        pass

    def pull_doc(self):
        pass

    def dump_json(self, name, entry):
        with open(name, 'a') as input:
            json.dump(entry,input,indent=4)

    def test_doc(self):
        try:
            self.service = build("docs", 'v1', credentials=self.creds)
            document = self.service.documents().get(
                documentId=os.getenv("TEST_FILE_ID"),
                includeTabsContent=True
            ).execute()
            print("Lets test this, here is the title: {title}".format(title=document.get('title')))
            
            for tab in document['tabs']:
                print(tab['tabProperties']['title'])
                if len(tab.get('childTabs', [])) > 0:
                    print("These have subtabs")
                    for subTab in tab['childTabs']:
                        print(subTab['tabProperties']['title'])
                        print(type(subTab['documentTab']['body']['content']))
                        self.dump_json("test.json", subTab['documentTab']['body']['content'])
        except HttpError as h:
            print(h)

test = DocHandler()
test.test_doc()

    