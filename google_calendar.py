# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Token Pickle
from os import path
import pickle

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

import dateutil.parser
import pytz


class calendarAPI:
    def __init__(self):
        self.service = self.getService()
        self.events = self.getEvents()
        self.colors = self.service.colors().get(fields="event").execute()
        self.tasks = self.getTasks()

    # Credentials

    def getCredentials(self):
        if path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)
            return credentials
        return None

    def attemptToResolveCredentials(self, credentials):
        credentialsExpiredAndRefreshTokenAvailable = (
            credentials and credentials.expired and credentials.refresh_token
        )
        if (
            credentialsExpiredAndRefreshTokenAvailable
        ):  # If there are valid credentials, try refresh.
            self.refreshCredentials(credentials)
        else:  # If there are no (valid) credentials available, let the user log in.
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server()
        self.saveCredentials(credentials)

    def refreshCredentials(self, credentials):
        credentials.refresh(Request())

    def saveCredentials(self, credentials):
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    # Service

    def getService(self):
        """ get google calender api service"""
        credentials = self.getCredentials()
        credentials_not_valid = not credentials or not credentials.valid
        if credentials_not_valid:
            self.attemptToResolveCredentials(credentials)
        service = build("calendar", "v3", credentials=credentials)
        return service

    # Events

    def getEvents(self):
        events_result = self.getEventsResult()
        events = events_result.get("items", [])
        return events

    def getEventsResult(self):
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=get_monday_of_this_week(),
                maxResults=NUMBER_OF_FUTURE_EVENTS,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result

    def getEventTime(self, event, time):
        """ get event time (start/end) and convert to datetime, timezone aware object """
        event_time = event[time].get("dateTime", event[time].get("date"))
        event_time = dateutil.parser.parse(event_time).replace(tzinfo=pytz.utc)
        return event_time

    # Tasks

    def getTasks(self):
        tasks = []
        if not self.events:
            return tasks
        for event in self.events:
            start = self.getEventTime(event, "start")
            end = self.getEventTime(event, "end")
            name = event["summary"]
            try:
                color_hexcode = self.colors["event"][event["colorId"]]["background"]
                color = self.getColorName(color_hexcode)
            except Exception as e:
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
