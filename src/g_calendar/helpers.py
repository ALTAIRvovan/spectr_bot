import datetime
import os
import pickle

from googleapiclient import discovery
from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow

import settings


def load_credentials():
    creds = None

    if os.path.exists(settings.GOOGLE_TOKEN_PATH):
        with open(settings.GOOGLE_TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                settings.GOOGLE_SCOPE)
            creds = flow.run_console() #run_local_server(port=0)
            # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def load_events_for_next_day():
    creds = load_credentials()
    service = discovery.build("calendar", "v3", credentials=creds)

    utc_now = datetime.datetime.utcnow()
    now = utc_now.isoformat() + 'Z'
    next_day = (utc_now + datetime.timedelta(days=1)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        timeMin=now, timeMax=next_day,
        singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])
    return events
