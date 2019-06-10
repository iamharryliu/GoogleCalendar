from config import activity_colors

from utils.events import getEvents
from utils.colors import colors, getColorName
from utils.time import one_week_from_now, getEventTime

events = getEvents()


class Task:
    total_time = 0

    def __init__(self, name, color, start=0, end=0):
        self.name = name
        self.start = start
        self.end = end
        self.color = color
        self.total_time = self.get_total_time()

    def get_total_time(self):
        if self.start == 0 or self.end == 0:
            return 0
        time = self.end - self.start
        time = time.total_seconds()  # datetime -> seconds
        time = time / 60 / 60  # seconds -> hours
        return time


def getTasks():
    tasks = []
    if not events:
        return tasks
    for event in events:
        start = getEventTime(event, 'start')
        end = getEventTime(event, 'end')
        event_less_than_one_week_from_now = end < one_week_from_now
        if event_less_than_one_week_from_now:
            name = event['summary']
            try:
                color_hexcode = colors['event'][event['colorId']]['background']
                color_hexcode = getColorName(color_hexcode)
            except Exception as e:
                color_hexcode = 'LAVENDAR'
            task = Task(name, color_hexcode, start, end)
            tasks.append(task)
    return tasks


def getActivityTime():
    tasks = getTasks()
    activity_time = dict()
    for color, activity in activity_colors.items():
        for task in tasks:
            if task.color == color:
                if activity in activity_time:
                    activity_time[activity]['total_time'] += task.total_time
                else:
                    activity_time[activity] = {'total_time': task.total_time}
    return activity_time


def getTotalTimeOfTasks():
    total_time = 0
    tasks = getTasks()
    for task in tasks:
        total_time += task.total_time
    return total_time


def getActivityPercent():
    total_time_of_tasks = getTotalTimeOfTasks()
    activity_time = getActivityTime()
    for activity, total_time in activity_time.items():
        percent = activity_time[activity]['total_time'] / total_time_of_tasks * 100
        percent = round(percent, 0)
        percent = int(percent)
        activity_time[activity]['percent'] = percent
    return activity_time


def getActivityData():
    activity_data = getActivityPercent()
    return activity_data
