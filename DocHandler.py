import os.path
import os
import json
from time import process_time as timer
from datetime import datetime
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv, find_dotenv, set_key
from pathlib import Path
from Event import Event, DocumentedEvent
from EventExceptions import BadEnvException
from Date import Date
from Month import Month
from Year import Year
from YearList import YearList
from EnvLists import required_list, optional_list
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
        self.start_time = timer()
        load_dotenv()
        verified, missing_req, missing_opt = self.verify_env()
        if not verified: 
            raise BadEnvException("Something is wrong with the env file!", missing_req, missing_opt)
        self.creds = None
        self.validate()
        self.test_doc()
        self.flush_to_database()
        self.set_metadata()
        DocHandler.num += 1

    def __del__(self):
        if DocHandler.num > 0:
            DocHandler.num -= 1

    def verify_env(self):
        missing_req = []
        missing_opt = []
        code = 1
        for req in required_list:
            if req not in os.environ:
                missing_req.append(req)
        for op in optional_list:
            if op in os.environ:
                setattr(self, op.lower(), os.getenv(op))
            else:
                missing_opt.append(op)
        if len(missing_req): code = 0
        return code, missing_req, missing_opt

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
        set_key(env_path, 'DOCUMENT_PULL_TIME', f'{timer() - self.start_time:.3f} secs')

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

    def process_subTab(self, subTab, month, path):
        for line in subTab['documentTab']['body']['content']:
            if 'paragraph' in line:
                if 'bullet' in line['paragraph']: # We are collecting events
                    element = line['paragraph']['elements'][0]
                    event_string = element['textRun']['content'].strip() #There should only be one
                    time_string, event_string = self.extract_time_string(event_string)
                    note_string = ''
                    duration_string = ''
                    if '[' in event_string and ']' in event_string:
                        note_string = event_string[event_string.index("["):event_string.rindex("]") + 1]
                        event_string = event_string.replace(note_string, '')
                    if '(' in event_string and ')' in event_string:
                        duration_string = event_string[event_string.rindex("("):event_string.rindex(")") + 1]
                        event_string = event_string.replace(duration_string, '')
                    #new_event = Event(event_string,time_string,duration_string[1:-1],note_string)
                    new_documented_event = DocumentedEvent(event_string,time_string,duration_string[1:-1],note_string)
                    new_documented_event.add_start_index(element['startIndex'])
                    new_documented_event.add_end_index(element['endIndex'])
                    new_date.append(new_documented_event)
                    event_path = f'{date_path}\\{new_documented_event.get_folder_name()}'
                    recording_path = f'{event_path}\\Recording'
                    notes_path = f'{event_path}\\Notes'
                    for each_path in [event_path, recording_path, notes_path]:
                        if not Path(each_path).is_dir():
                            Path(each_path).mkdir(exist_ok=True)
                    #events_list.append(new_event)
                else: # We are now collecting days
                    text = line['paragraph']['elements'][0]['textRun']['content'].strip()
                    if text != '': 
                        month_string = text.split()[0]
                        date_string = text.split()[-1][:-2].strip()
                        new_date = Date(month_string, int(date_string))
                        date_path = f'{path}\\{new_date.date_num} {new_date.day_name}'
                        if not Path(date_path).is_dir():
                            Path(date_path).mkdir(exist_ok=True)
                        month.append(new_date)



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
                year_path = f'{os.getenv('STORAGE_PATH')}\\{new_year.number}'
                if not Path(year_path).is_dir():
                    Path(year_path).mkdir(exist_ok=True)
                for subTab in tab.get('childTabs', []):
                    new_month = Month(subTab['tabProperties']['title'])
                    month_path = f'{year_path}\\{new_month.month}'
                    if not Path(month_path).is_dir():
                        Path(month_path).mkdir(exist_ok=True)
                    new_year.append(new_month) #new_year.add_month(new_month)
                    #print(new_month.year_num)
                    self.process_subTab(subTab, new_month, month_path)
                database.append(new_year) #database.add_year(new_year)
            
            self.database = database
        except HttpError as h:
            print(h)


#test = DocFactory()
#test.test_doc()
#print(test.test_doc())
#print(test.database)
#test.flush_to_database()