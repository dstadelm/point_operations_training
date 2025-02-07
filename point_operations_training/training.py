import json
import sys
from datetime import datetime
from pathlib import Path
from random import randint
from point_operations_training.timer import Timer

import matplotlib.pyplot as plt

LEARN_INTERVAL = 20
TRAIN_INTERVAL = 20
SELECTION_FRACTION = 0.2

UP_ONE_LINE = "\033[A"  # up 1 line
DELETE_LINE = "\033[K"  # clear line


def teach():
    print("##############")
    print("Teach Values")
    print("##############")
    _ = input("Start")
    timer = Timer(name="measure")

    result_times: dict[float, tuple[int, int]] = {}

    for _ in range(LEARN_INTERVAL):
        x = randint(1, 9)
        y = randint(1, 9)
        _ = input(f"{x} * {y}")
        duration = timer.duration()
        result_times[duration] = (x, y)
        _ = sys.stdout.write(UP_ONE_LINE)
        _ = sys.stdout.write(DELETE_LINE)

    return result_times


def train(train_values: list[tuple[int, int]]):
    print("##############")
    print(" Train Values")
    print("##############")
    prev_idx = 0
    idx = 0
    for _ in range(TRAIN_INTERVAL):
        while idx == prev_idx:
            idx = randint(0, len(train_values) - 1)
        prev_idx = idx
        x = train_values[idx][0]
        y = train_values[idx][1]
        _ = input(f"{x} * {y}")
        _ = sys.stdout.write(UP_ONE_LINE)
        _ = sys.stdout.write(DELETE_LINE)


def display_stats():
    stats_file = Path("stats.json")
    data: dict[str, list[dict[str, str | float]]] = {}
    if stats_file.is_file():
        with open("stats.json") as stats:
            data = json.load(stats)

    date_series = [val["date"] for val in data["stats"]]
    avg_series = [val["avg"] for val in data["stats"]]
    max_series = [val["max"] for val in data["stats"]]
    min_series = [val["min"] for val in data["stats"]]

    _, ax = plt.subplots()  # pyright: ignore [reportUnknownMemberType]
    (avg_plot,) = ax.plot(  # pyright: ignore [reportUnknownMemberType]
        date_series, avg_series
    )
    (max_plot,) = ax.plot(  # pyright: ignore [reportUnknownMemberType]
        date_series, max_series
    )
    (min_plot,) = ax.plot(  # pyright: ignore [reportUnknownMemberType]
        date_series, min_series
    )
    _ = ax.legend(  # pyright: ignore [reportUnknownMemberType]
        (avg_plot, max_plot, min_plot),
        ("avg", "max", "min"),
        loc="upper right",
        shadow=True,
    )
    plt.show()  # pyright: ignore [reportUnknownMemberType]


def gen_stats(times: dict[float, tuple[int, int]]) -> dict[str, str | float]:
    sorted_times = dict(sorted(times.items()))
    sum = 0
    max = 0
    min = 100
    for t in sorted_times.keys():
        sum += t
        if t > max:
            max = t
        if t < min:
            min = t

    avg = sum / len(sorted_times)

    entry = {
        "date": str(datetime.now()),
        "avg": float(f"{avg:.2f}"),
        "max": float(f"{max:.2f}"),
        "min": float(f"{min:.2f}"),
    }
    return entry


def get_train_values(times: dict[float, tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_times = dict(sorted(times.items()))
    num_values = round(len(sorted_times) * SELECTION_FRACTION)
    train_values = list(sorted_times.values())[-num_values:]
    return train_values


def main():
    result_times = teach()

    entry = gen_stats(result_times)
    data: dict[str, list[dict[str, str | float]]] = {}

    stats_file = Path("stats.json")

    if stats_file.is_file():
        with open("stats.json") as stats:
            data = json.load(stats)

    if "stats" in data:
        data["stats"].append(entry)
    else:
        data = {"stats": []}
        data["stats"].append(entry)

    with open("stats.json", "w") as stats:
        json.dump(data, stats)

    print(f"Avg: {entry['avg']:.2}, Max = {entry['max']:.2}, Min = {entry['min']:.2}")

    train(get_train_values(result_times))

    display_stats()
