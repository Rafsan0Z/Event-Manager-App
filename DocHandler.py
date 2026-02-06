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
from Month import Month
import shelve

def DocFactory():
    try:
        new_handler = DocHandler()
    except RuntimeError as r:
        print("You cant request any more handlers!!")
    else:
        return new_handler

class DocHandler:

    num = 0

    def __new__(cls, *args, **kargs):
        if DocHandler.num > 0:
            raise RuntimeError("You cannot create any more handlers!")
        else:
            return super().__new__(cls)

    def __init__(self):
        load_dotenv()
        self.creds = None
        self.validate()
        DocHandler.num += 1

    def __del__(self):
        DocHandler.num -= 1

    def flush_to_database(yearlist):
        with shelve.open("Event_DB") as db:
            db['YearList'] = yearlist

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
    
    def extract_time_string(self, event_string):
        time_string = event_string[:event_string.index(':') + 1]
        event_string = event_string.replace(time_string, '')
        if event_string[0] != ' ':
            extra_time_string = event_string[:event_string.index(':') + 1]
            time_string += extra_time_string
            event_string = event_string.replace(extra_time_string, '')
        print(time_string[:-1])
        return event_string

    def process_subTab(self, subTab):
        test_string = ""
        new_month = Month(subTab['tabProperties']['title'])
        for line in subTab['documentTab']['body']['content']:
            if 'paragraph' in line:
                if 'bullet' in line['paragraph']:
                    event_string = line['paragraph']['elements'][0]['textRun']['content'].strip() #There should only be one
                    print(event_string)
                    event_string = self.extract_time_string(event_string)
                    note_string = ''
                    duration_string = ''
                    if '[' in event_string and ']' in event_string:
                        note_string = event_string[event_string.index("["):event_string.rindex("]") + 1]
                        event_string = event_string.replace(note_string, '')
                    if '(' in event_string and ')' in event_string:
                        duration_string = event_string[event_string.index("("):event_string.rindex(")") + 1]
                        event_string = event_string.replace(duration_string, '')
                    print(note_string)
                    print(duration_string)
                    print(event_string)
                else:
                    month_string = line['paragraph']['elements'][0]['textRun']['content'].strip()
                    print(month_string)
        return test_string




    def test_doc(self):
        try:
            self.service = build("docs", 'v1', credentials=self.creds)
            document = self.service.documents().get(
                documentId=os.getenv("TEST_FILE_ID"),
                includeTabsContent=True
            ).execute()
            print("Lets test this, here is the title: {title}".format(title=document.get('title')))
            
            for tab in document['tabs'][1:]:
                print(tab['tabProperties']['title'])
                if len(tab.get('childTabs', [])) > 0:
                    print("These have subtabs")
                    for subTab in tab['childTabs']:
                        print(subTab['tabProperties']['title'])
                        self.process_subTab(subTab)
                        #self.dump_json("test.json", subTab['documentTab']['body']['content'])
        except HttpError as h:
            print(h)


test = DocFactory()
test.test_doc()