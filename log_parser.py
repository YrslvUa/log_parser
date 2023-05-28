from collections import defaultdict
from datetime import datetime


class Parser:
    def __init__(self, file):
        self.file = file

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def log_parser(self):
        nok_counts, ok_counts = defaultdict(int), defaultdict(int)
        with open(self.file, "r") as file:
            for line in file:
                timestamp = line.split("]")[0].strip("[")
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                day_key = dt.strftime("%Y-%m-%d")
                if "NOK" in line:
                    nok_counts[day_key] += 1
                else:
                    ok_counts[day_key] += 1

        with open("log_counts.txt", "w") as file:
            for key, count in nok_counts.items():
                file.write(f"NOK : [{key}] {count}\n")
            for key, count in ok_counts.items():
                file.write(f"OK : [{key}] {count}\n")


if __name__ == "__main__":
    grouped_events = Parser(file='events.txt')
    grouped_events.log_parser()
