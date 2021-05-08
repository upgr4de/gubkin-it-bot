import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from data.config import GOOGLE_CREDENTIALS, GOOGLE_TOKEN


#при изменении скопа, необходимо удалить автоматически создающийся токен-файл
scopes = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/script.projects']


def login():
    try:
        creds = None

        # The file google_token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(GOOGLE_TOKEN):
            with open(GOOGLE_TOKEN, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, scopes)
                creds = flow.run_local_server(port = 0)
            
            # Save the credentials for the next run
            with open(GOOGLE_TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        service = build('script', 'v1', credentials = creds)

        pprint('Login successful')

        return service
    except Exception as e:
        pprint(f'Login failure: {e}')
        
        return None
