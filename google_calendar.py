from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import path
import pickle, dateutil.parser, pytz
from config import NUMBER_OF_FUTURE_EVENTS, SCOPES, ACTIVITY_COLORS
from utils import (
    COLOR_ID_TO_COLOR_DICT,
    get_monday_of_this_week,
    get_today,
    get_one_week_from_today,
    Task,
    getStartOfWeekX,
    getEndOfWeekX,
)


class calendar_api:
    def __init__(self):
        self.credentials = self.get_api_credentials()
        self.service = self.get_google_api_service()
        self.tasks = self.get_tasks_from_service()

    def get_api_credentials(self):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
        if credentials and credentials.valid:
            return credentials
        else:
            return self.resolve_credentials(credentials)

    def resolve_credentials(self, credentials):
        try:
            credentials.refresh(Request())
        except:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server()
        finally:
            self.save_credentials(credentials)
            return credentials

    def save_credentials(self, credentials):
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    def get_google_api_service(self):
        return build("calendar", "v3", credentials=self.credentials)

    def get_tasks_from_service(self):
        tasks = []
        events = self.get_events_from_service()
        # colors = self.service.colors().get(fields="event").execute()
        for event in events:
            start = self.get_event_start_time(event)
            end = self.get_event_end_time(event)
            if "colorId" in event:
                # color_hexcode = colors["event"][event["colorId"]]["background"]
                color_id = event["colorId"]
                color = COLOR_ID_TO_COLOR_DICT[color_id]
            else:
                color = "GRAPHITE"
            task = Task(color, start, end)
            tasks.append(task)
        return tasks

    def get_events_from_service(self):
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
        events = events_result.get("items", [])
        return events

    def get_event_start_time(self, event):
        time = event["start"].get("dateTime", event["start"].get("date"))
        return self.get_time_with_timezone(time)

    def get_event_end_time(self, event):
        time = event["end"].get("dateTime", event["end"].get("date"))
        return self.get_time_with_timezone(time)

    def get_time_with_timezone(self, time):
        return dateutil.parser.parse(time).replace(tzinfo=pytz.utc)

    def get_tasks_for_this_week(self):
        tasks = []
        start_of_week = getStartOfWeekX(1)
        start_of_next_week = getStartOfWeekX(2)
        for task in self.tasks:
            if start_of_week <= task.start and task.start < start_of_next_week:
                tasks.append(task)
        return tasks

    def getTasksForWeekX(self, week):
        tasks = []
        start = getStartOfWeekX(week)
        end = getEndOfWeekX(week)
        for task in self.tasks:
            task_in_week_X = start <= task.start and task.start <= end
            if task_in_week_X:
                tasks.append(task)
        return tasks

    def get_activity_time_for_tasks(self, tasks):
        activity_time = dict()
        for color, activity in ACTIVITY_COLORS.items():
            if activity:
                activity_time[activity] = 0
            for task in tasks:
                if task.color == color:
                    if activity in activity_time:
                        activity_time[activity] += task.total_time
                    else:
                        activity_time[activity] = task.total_time
        return activity_time

    def get_pie_chart_data_for_week(self):
        tasks = self.get_tasks_for_this_week()
        activity_time = self.get_activity_time_for_tasks(tasks)
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
            activity_time = self.get_activity_time_for_tasks(tasks)
            for activity, time in activity_time.items():
                if activity not in legend:
                    legend.append(activity)
                week.append(time)
            data.append(week)
        data.insert(0, legend)
        return data
