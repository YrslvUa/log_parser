from time import time
from collections import defaultdict
from datetime import datetime


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time()
        result = func(*args, **kwargs)
        ended_at = time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Function {func.__name__} worked {elapsed} sec.')
        return result

    return surrogate


class Parser:
    def __init__(self, file):
        self.file, self.file_obj = file, None
        self.counts = defaultdict(lambda: defaultdict(int))

    def __iter__(self):
        self.file_obj = open(self.file, "r")
        return self

    def __next__(self):
        line = self.file_obj.readline()
        if not line:
            self.file_obj.close()
            raise StopIteration

        timestamp = line.split("]")[0].strip("[")
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        day_key = dt.strftime("%Y-%m-%d")
        event_type = "NOK" if "NOK" in line else "OK"

        self.counts[day_key][event_type] += 1

        return day_key, event_type

    @time_track
    def log_parser(self):
        for _ in self:
            pass

        with open("log_counts.txt", "w") as file:
            for day_key, events in self.counts.items():
                file.write(f"NOK : [{day_key}] {events['NOK']}\n")
                file.write(f"OK : [{day_key}] {events['OK']}\n")


if __name__ == "__main__":
    grouped_events = Parser(file='events.txt')
    grouped_events.log_parser()
