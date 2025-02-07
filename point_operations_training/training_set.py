from functools import wraps
from typing import Callable, TypeVar
from datetime import datetime
from random import randint
from point_operations_training.timer import Timer


T = TypeVar("T", bound="RandValStats")
R = TypeVar("R")


def method_cache(func: Callable[[T], R]) -> Callable[[T], R]:
    cache: dict[str, R] = {}

    @wraps(func)
    def wrapper(self: T) -> R:
        if "result" in cache:
            return cache["result"]

        result = func(self)
        cache["result"] = result
        return result

    return wrapper


class RandValStats:

    SELECTION_FRACTION: float = 0.2

    def __init__(self) -> None:
        self.stats: dict[float, tuple[int, int]] = {}
        self.timer: Timer = Timer(name="rand_val_time")
        self.value: tuple[int, int] = (0, 0)
        self.train_values: list[tuple[int, int]] = []
        self.prev_idx: int = -1

    def next(self) -> tuple[int, int]:
        if self.value == (0, 0):
            self.timer.start()
        else:
            self.stats[self.timer.duration()] = self.value

        self.value = (randint(1, 9), randint(1, 9))
        return self.value

    def sorted(self) -> dict[float, tuple[int, int]]:
        return dict(sorted(self.stats.items()))

    def statistics(self) -> dict[str, str | float]:
        sum = 0
        max = 0
        min = 100
        for t in self.stats.keys():
            sum += t
            if t > max:
                max = t
            if t < min:
                min = t

        avg = sum / len(self.stats)

        entry = {
            "date": str(datetime.now()),
            "avg": float(f"{avg:.2f}"),
            "max": float(f"{max:.2f}"),
            "min": float(f"{min:.2f}"),
        }
        return entry

    @method_cache
    def slowest_n_percent_values(self) -> list[tuple[int, int]]:
        num_values = round(len(self.stats) * RandValStats.SELECTION_FRACTION)
        data = list(self.sorted().values())[-num_values:]
        return data

    def next_train_val(self) -> tuple[int, int]:
        idx = randint(0, len(self.slowest_n_percent_values()) - 1)
        while idx == self.prev_idx:
            idx = randint(0, len(self.slowest_n_percent_values()) - 1)

        self.prev_idx = idx
        return self.slowest_n_percent_values()[idx]
