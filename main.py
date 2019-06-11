from google_calendar import calendarAPI


def main():
    calendar_api = calendarAPI()
    calendar_api.getColumnChartDataForNext4Weeks()

if __name__ == "__main__":
    main()
