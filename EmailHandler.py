from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

def EmailFactory():
    try:
        handler = EmailHandler()
    except Exception as e:
        print(e)
    else:
        return handler

class EmailHandler:

    def _init_(self):
        pass

    
