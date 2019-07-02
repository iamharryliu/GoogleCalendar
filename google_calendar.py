# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Token Pickle
from os import path
import pickle

import dateutil.parser
import pytz

from config import NUMBER_OF_FUTURE_EVENTS, SCOPES, ACTIVITY_COLORS
from utils import (
    HEXCODE_TO_COLOR_DICT,
    get_monday_of_this_week,
    get_today,
    get_one_week_from_today,
    Task,
    getStartOfWeekX,
    getEndOfWeekX,
)


class calendarAPI:
    def __init__(self):
        self.tasks = self.getTasks()

    # Service

    def getService(self):
        credentials = self.getCredentials()
        if not credentials.valid:
            self.resolveCredentials(credentials)
        service = build("calendar", "v3", credentials=credentials)
        return service

    # Credentials

    def getCredentials(self):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
        return credentials

    def resolveCredentials(self, credentials):
        try:
            self.refreshCredentials(credentials)
        except:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server()
        finally:
            self.saveCredentials(credentials)

    def refreshCredentials(self, credentials):
        credentials.refresh(Request())

    def saveCredentials(self, credentials):
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    # Events

    def getEventsFromService(self, service):
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=get_monday_of_this_week(),
                maxResults=NUMBER_OF_FUTURE_EVENTS,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    def getEventTime(self, event, time):
        """ get event time (start/end) and convert to datetime, timezone aware object """
        event_time = event[time].get("dateTime", event[time].get("date"))
        event_time = dateutil.parser.parse(event_time).replace(tzinfo=pytz.utc)
        return event_time

    def getEventStartTime(self, event):
        time = event["start"].get("dateTime", event["start"].get("date"))
        time = self.addTimezone(time)
        return time

    def getEventEndTime(self, event):
        time = event["end"].get("dateTime", event["end"].get("date"))
        time = self.addTimezone(time)
        return time

    def addTimezone(self, time):
        time = dateutil.parser.parse(time).replace(tzinfo=pytz.utc)
        return time

    # Tasks

    def getTasks(self):
        service = self.getService()
        tasks = self.getTasksFromService(service)
        return tasks

    def getTasksFromService(self, service):
        tasks = []
        events = self.getEventsFromService(service)
        colors = service.colors().get(fields="event").execute()
        for event in events:
            name = event["summary"]
            start = self.getEventStartTime(event)
            end = self.getEventEndTime(event)
            try:
                color_hexcode = colors["event"][event["colorId"]]["background"]
                color = self.getColorName(color_hexcode)
            except:
                print(f"{name} uses other color")
                color = "LAVENDAR"
            task = Task(name, color, start, end)
            tasks.append(task)
        return tasks

    def getTasksForNext7Days(self):
        tasks = []
        for task in self.tasks:
            task_less_than_one_week_from_today = (
                get_today() <= task.start and task.end <= get_one_week_from_today()
            )
            if task_less_than_one_week_from_today:
                tasks.append(task)
        return tasks

    def getTasksForWeekX(self, week):
        tasks = []
        start = getStartOfWeekX(week)
        end = getEndOfWeekX(week)
        for task in self.tasks:
            task_in_week_X = start <= task.start and task.end <= end
            if task_in_week_X:
                tasks.append(task)
        return tasks

    def getColorName(self, hexcode):
        """ hex code color -> name of color """
        if hexcode in HEXCODE_TO_COLOR_DICT:
            return HEXCODE_TO_COLOR_DICT[hexcode]

    def getActivityTimeForTasks(self, tasks):
        activity_time = dict()
        for color, activity in ACTIVITY_COLORS.items():
            if activity != "":
                activity_time[activity] = 0
            for task in tasks:
                if task.color == color:
                    if activity in activity_time:
                        activity_time[activity] += task.total_time
                    else:
                        activity_time[activity] = task.total_time
        return activity_time

    # Data

    def getPieChartDataForNext7Days(self):
        tasks = self.getTasksForNext7Days()
        activity_time = self.getActivityTimeForTasks(tasks)
        data = [["activity", "time spent"]]
        for activity, time in activity_time.items():
            activity_time = [activity, time]
            data.append(activity_time)
        return data

    def getColumnChartDataForNextXWeeks(self, x_weeks):
        data = []
        legend = ["Week"]
        for week in range(1, x_weeks + 1):
            tasks = self.getTasksForWeekX(week)
            week = [str(week)]
            activity_time = self.getActivityTimeForTasks(tasks)
            for activity, time in activity_time.items():
                if activity not in legend:
                    legend.append(activity)
                week.append(time)
            data.append(week)
        data.insert(0, legend)
        return data
