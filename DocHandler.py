import os.path
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv, find_dotenv, set_key
from pathlib import Path
from Event import Event
from Date import Date
from Month import Month
from Year import Year
from YearList import YearList
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
        self.test_doc()
        self.flush_to_database()
        self.set_metadata()
        DocHandler.num += 1

    def __del__(self):
        DocHandler.num -= 1

    def flush_to_database(self):
        with shelve.open("Event_DB") as db:
            db['YearList'] = self.database
        db.close()

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



    def set_metadata(self):
        drive = build('drive', 'v3', credentials=self.creds)
        metadata = drive.files().get(
            fileId = os.getenv("TEST_FILE_ID"),
            fields='name, modifiedTime'
        ).execute()

        unformatted_time = metadata.get('modifiedTime')
        utc_time = datetime.fromisoformat(unformatted_time.replace('Z', '+00:00'))
        est_zone = ZoneInfo(os.getenv('TIME_ZONE'))
        est_time = utc_time.astimezone(est_zone)

        env_path = find_dotenv()
        set_key(env_path, "LAST_MODIFIED", est_time.strftime('%Y-%m-%d %I:%M %p'))
        set_key(env_path, 'FILE_NAME', metadata.get('name'))

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
        #print(time_string[:-1])
        return time_string[:-1], event_string

    def process_subTab(self, subTab, month):
        test_string = ""
        events_list = []
        for line in subTab['documentTab']['body']['content']:
            if 'paragraph' in line:
                if 'bullet' in line['paragraph']: # We are collecting events
                    event_string = line['paragraph']['elements'][0]['textRun']['content'].strip() #There should only be one
                    #print(event_string)
                    time_string, event_string = self.extract_time_string(event_string)
                    note_string = ''
                    duration_string = ''
                    if '[' in event_string and ']' in event_string:
                        note_string = event_string[event_string.index("["):event_string.rindex("]") + 1]
                        event_string = event_string.replace(note_string, '')
                    if '(' in event_string and ')' in event_string:
                        duration_string = event_string[event_string.rindex("("):event_string.rindex(")") + 1]
                        event_string = event_string.replace(duration_string, '')
                    #print(note_string)
                    #print(duration_string[1:-1])
                    #print(event_string)
                    new_event = Event(event_string,time_string,duration_string[1:-1],note_string)
                    new_date.append(new_event)
                    events_list.append(new_event)
                else: # We are now collecting days
                    text = line['paragraph']['elements'][0]['textRun']['content'].strip()
                    if text != '': 
                        month_string = text.split()[0]
                        date_string = text.split()[-1][:-2].strip()
                        #print(month_string, date_string)
                        new_date = Date(month_string, int(date_string))
                        month.append(new_date)
                        #we add this date to the month
                #break




    def test_doc(self):
        try:
            self.service = build("docs", 'v1', credentials=self.creds)
            document = self.service.documents().get(
                documentId=os.getenv("TEST_FILE_ID"),
                includeTabsContent=True
            ).execute()            
            database = YearList()

            for tab in document['tabs'][1:]:
                new_year = Year(int(tab['tabProperties']['title']))
                for subTab in tab.get('childTabs', []):
                    new_month = Month(subTab['tabProperties']['title'])
                    new_year.append(new_month) #new_year.add_month(new_month)
                    self.process_subTab(subTab, new_month)
                database.append(new_year) #database.add_year(new_year)
            
            self.database = database
        except HttpError as h:
            print(h)


#test = DocFactory()
#test.test_doc()
#print(test.test_doc())
#print(test.database)
#test.flush_to_database()