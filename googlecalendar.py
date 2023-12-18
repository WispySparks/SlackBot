from datetime import datetime

import requests as r

from secret import googleClientId, googleClientSecret, googleRefreshToken


class GoogleCalendar(): # Still need to implement getting a new access token when old one is expired
    
    headers: dict[str, str] = {"Authorization": "Bearer "}
    calendars: dict[str, str] = {}
    
    def __init__(self) -> None:
        self.getAccessToken()
        self.getCalendars()

    def getAccessToken(self) -> None:
        endpoint = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": googleClientId,
            "client_secret": googleClientSecret,
            "refresh_token": googleRefreshToken,
            "grant_type": "refresh_token"
        }
        resp = r.post(endpoint, payload)
        json = resp.json()
        if (json.get("access_token") != None):
            self.headers = {"Authorization": "Bearer " + json.get("access_token")}
            
    def getCalendars(self) -> None:
        endpoint = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
        resp = r.get(endpoint, headers=self.headers)
        items = resp.json().get("items")
        for calendar in items:
            name = calendar.get("summary")
            id = calendar.get("id")
            self.calendars.update({name: id})
            
    def getEvents(self, calendarName) -> list[tuple[str, datetime]]:
        events = []
        id = self.calendars.get(calendarName)
        if (id == None): return events
        endpoint = "https://www.googleapis.com/calendar/v3/calendars/" + id + "/events"
        payload = {
            "orderBy": "startTime",
            "singleEvents": True,
            "timeMin": datetime.now().astimezone().isoformat()
        }
        resp = r.get(endpoint, payload, headers=self.headers)
        items = resp.json().get("items")
        for event in items:
            name = event.get("summary")
            start = event.get("start").get("date") if event.get("start").get("dateTime") == None else event.get("start").get("dateTime")
            date = datetime.fromisoformat(start)
            events.append((name, date))
        return events
    
    def getNextEvent(self, calendarName) -> tuple[str, datetime] | None:
        events = self.getEvents(calendarName)
        if len(events) < 1: return None
        return events[0]
        