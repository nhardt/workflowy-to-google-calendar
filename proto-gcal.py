#!/usr/bin/env python3


import os
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# The scopes required for accessing the calendar API
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
]
CREDENTIALS_FILE = ".gcal.credentials.json"
TOKEN_FILE = ".gcal.token.json"


def main():
    get_calendar_events()


def get_calendar_events():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    calendar_list = service.calendarList().list(pageToken=None).execute()
    print(calendar_list)
    for calendar_list_entry in calendar_list["items"]:
        print(calendar_list_entry["summary"])

    # events_result = service.events().list(
    #    calendarId="primary", maxResults=10).execute()
    # events = events_result.get("items", [])
    # if not events:
    #     print("No upcoming events found.")
    # for event in events:
    #     start = event["start"].get("dateTime", event["start"].get("date"))
    #     print(f'{start} - {event["summary"]}')


if __name__ == "__main__":
    main()
