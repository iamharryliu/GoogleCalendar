from datetime import datetime, timedelta
import dateutil.parser
import pytz

# Now and start of week.
now = datetime.utcnow()
days_into_the_week = timedelta(now.weekday())
start_of_week = (now - days_into_the_week).isoformat() + 'Z'  # 'Z' indicates UTC time

# One week from now.
seven_days = timedelta(days=7)
one_week_from_now = now + seven_days
one_week_from_now = one_week_from_now.replace(tzinfo=pytz.utc)


def getEventTime(event, time):
    ''' get event time (start/end) and convert to datetime, timezone aware object '''
    event_time = event[time].get('dateTime', event[time].get('date'))
    event_time = dateutil.parser.parse(event_time).replace(tzinfo=pytz.utc)
    return event_time
