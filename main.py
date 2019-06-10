from utils.output import printTasks
from utils.tasks import getActivityData


def main():
    # printTasks()
    activity_data = getActivityData()
    print(activity_data)


if __name__ == '__main__':
    main()
