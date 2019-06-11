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
        return f'{self.name}: {self.color}'
