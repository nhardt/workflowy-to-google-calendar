#!/usr/bin/env python3

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
]
CREDENTIALS_FILE = ".gcal.credentials.json"
TOKEN_FILE = ".gcal.token.json"


class GCal:
    def __init__(self):
        self.service = self.make_calendar_service()
        self.workflowy_calendar_id = self.get_calendar_id("workflowy")

    def make_calendar_service(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        return build("calendar", "v3", credentials=creds)

    def get_calendar_id(self, calendar_name):
        calendar_list = self.service.calendarList().list(pageToken=None).execute()
        for calendar_list_entry in calendar_list["items"]:
            if calendar_list_entry["summary"] == "workflowy":
                return calendar_list_entry["id"]
        raise Exception("workflowy calendar not found")

    def get_events(self):
        events_result = (
            self.service.events()
            .list(calendarId=self.workflowy_calendar_id, maxResults=10)
            .execute()
        )
        return events_result.get("items", [])

    def get_event(self, uuid):
        uuid = uuid.replace("-", "")
        try:
            return (
                self.service.events()
                .get(calendarId=self.workflowy_calendar_id, eventId=uuid)
                .execute()
            )
        except:
            return None

    def insert_event(self, uuid, summary, start, end):
        print(f"inserting event '{uuid}' {summary} {start} {end}")
        uuid = uuid.replace("-", "")
        event = {
            "id": uuid,
            "summary": summary,
            "location": "",
            "description": "",
            "start": {
                "dateTime": start,
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": end,
                "timeZone": "America/Los_Angeles",
            },
            "reminders": {
                "useDefault": False,
            },
        }
        self.service.events().insert(
            calendarId=self.workflowy_calendar_id, body=event
        ).execute()
        # print(f"Event created: {event.get('htmlLink')}")

    def update_event(self, uuid, summary, start, end):
        print(f"update event '{uuid}' {summary} {start} {end}")
        uuid = uuid.replace("-", "")
        event = {
            "id": uuid,
            "summary": summary,
            "location": "",
            "description": "",
            "start": {
                "dateTime": start,
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": end,
                "timeZone": "America/Los_Angeles",
            },
            "reminders": {
                "useDefault": False,
            },
        }
        self.service.events().update(
            calendarId=self.workflowy_calendar_id, eventId=uuid, body=event
        ).execute()
