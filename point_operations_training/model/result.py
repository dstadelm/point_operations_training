from datetime import datetime
from typing import Protocol


class Result:
    def __init__(
        self,
        date: str = "",
        avg: float = 0,
        max: float = 0,
        min: float = 0,
    ) -> None:
        self.date: str = str(datetime.now())
        self.avg: float = avg
        self.max: float = max
        self.min: float = min


ResultCollectionType = list[dict[str, str | float]]


class ResultCollectionProtocol(Protocol):
    def avg_series(self) -> list[float]: ...
    def max_series(self) -> list[float]: ...
    def min_series(self) -> list[float]: ...


class ResultCollection:
    def __init__(self) -> None:
        self.results: list[Result] = []

    def add_result(self, result: Result) -> None:
        self.results.append(result)

    def sort_by_date(self) -> None:
        self.results.sort(key=lambda r: r.date)

    def avg_series(self) -> list[float]:
        self.sort_by_date()
        return [r.avg for r in self.results]

    def max_series(self) -> list[float]:
        self.sort_by_date()
        return [r.max for r in self.results]

    def min_series(self) -> list[float]:
        self.sort_by_date()
        return [r.min for r in self.results]

    def to_dict(self) -> ResultCollectionType:
        return [
            {
                "date": r.date,
                "avg": r.avg,
                "max": r.max,
                "min": r.min,
            }
            for r in self.results
        ]

    def from_dict(self, data: ResultCollectionType) -> None:
        for d in data:
            r = Result(
                str(d["date"]),
                float(d["avg"]),
                float(d["max"]),
                float(d["min"]),
            )
            self.add_result(r)
