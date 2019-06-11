from datetime import datetime, timedelta, date
import pytz

# Now and start of week.
now = datetime.utcnow()
today = date.today()
days_into_the_week = timedelta(now.weekday())
monday_of_this_week = today - days_into_the_week
monday_of_this_week = datetime.combine(monday_of_this_week, datetime.min.time()).isoformat() + 'Z'

# monday_of_this_week = monday_of_this_week.isoformat() + "Z"  # 'Z' indicates UTC time

# One week from now time aware.
seven_days = timedelta(days=7)
one_week_from_now = now + seven_days
one_week_from_now = one_week_from_now.replace(tzinfo=pytz.utc)

def startOfWeekX(week):
    start = today - timedelta(days=now.weekday()) + timedelta(weeks=week-1)
    start = datetime.combine(start, datetime.min.time()).replace(tzinfo=pytz.utc)
    return start

def endOfWeekX(week):
    start = startOfWeekX(week)
    end = start + seven_days
    return end

hexcode_to_color_dict = {
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

    def __repr__(self):
        return f"{self.name} / {self.color} / {self.start} / {self.end} / {self.total_time}"

