from google_calendar import calendarAPI


def main():
    calendar_api = calendarAPI()
    print(calendar_api.getActivityPieChartData())


if __name__ == "__main__":
    main()
