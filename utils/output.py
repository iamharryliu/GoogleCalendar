from utils.tasks import getActivityTime


def printTasks():
    activity_time = getActivityTime()
    for activity, values in activity_time.items():
        text = f"For {activity} you have planned to spend:"
        number_of_spaces = 15
        number_of_spaces -= len(activity)
        string_length = len(text) + number_of_spaces    # will be adding 10 extra spaces
        string_revised = text.ljust(string_length)
        printLineBreak()
        print(f'{string_revised} {values["total_time"]} hrs this week')
    printLineBreak()


def printLineBreak():
    print("\n-----------------------------------------------------------------")
