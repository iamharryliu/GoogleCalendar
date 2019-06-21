""" Time """


from config import START_OF_DAY
from datetime import datetime, timedelta, date
import pytz


def get_today():
    today = date.today()
    today = datetime.combine(today, datetime.min.time()).replace(tzinfo=pytz.utc)
    today = today + timedelta(hours=START_OF_DAY)
    return today


def get_one_week_from_today():
    today = get_today()
    one_week_from_today = today + timedelta(days=7)
    return one_week_from_today


def get_monday_of_this_week():
    today = get_today()
    days_into_the_week = timedelta(today.weekday())
    monday_of_this_week = today - days_into_the_week
    monday_of_this_week = (
        datetime.combine(monday_of_this_week, datetime.min.time()).isoformat() + "Z"
    )  # 'Z' indicates UTC time
    return monday_of_this_week


def getStartOfWeekX(week):
    today = get_today()
    start = today - timedelta(days=today.weekday()) + timedelta(weeks=week - 1)
    return start


def getEndOfWeekX(week):
    start = getStartOfWeekX(week)
    end = start + timedelta(days=7)
    return end


""" Task """


class Task:
    total_time = 0

    def __init__(self, name, color, start=0, end=0):
        self.name = name
        self.start = start
        self.end = end
        self.color = color
        self.total_time = self.get_total_time()

    def get_total_time(self):
        # if self.start == 0 or self.end == 0:
        #     return 0
        time = self.end - self.start
        time = time.total_seconds()  # datetime -> seconds
        time = time / 3600  # seconds -> hours
        return time

    def __repr__(self):
        return f"{self.name} / {self.color} / {self.start} / {self.end} / {self.total_time}"


HEXCODE_TO_COLOR_DICT = {
    "#a4bdfc": "LAVENDER",
    "#5484ed": "BLUEBERRY",
    "#46d6db": "PEACOCK",
    "#7ae7bf": "SAGE",
    "#51b749": "BASIL",
    "#ffb878": "TANGERINE",
    "#fbd75b": "BANANA",
    "#ff887c": "FLAMINGO",
    "#dc2127": "TOMATO",
    "#dbadff": "GRAPE",
    "#e1e1e1": "GRAPHITE",
}
