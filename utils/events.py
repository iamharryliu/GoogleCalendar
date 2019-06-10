from config import NUMBER_OF_FUTURE_EVENTS
from utils.google_calendar_api import getService
from utils.time import start_of_week

service = getService()


def getEvents():
    events_result = getEventsResult()
    events = events_result.get('items', [])
    return events


def getEventsResult():
    events_result = service.events().list(calendarId='primary', timeMin=start_of_week,
                                          maxResults=NUMBER_OF_FUTURE_EVENTS, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result
