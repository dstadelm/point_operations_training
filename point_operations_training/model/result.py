from datetime import datetime

from point_operations_training.model.session import Session


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


def result_from_session(session: Session) -> Result:
    return Result(
        session.date,
        session._assignments.avg_time(),
        session._assignments.max_time(),
        session._assignments.min_time(),
    )


ResultCollectionType = list[dict[str, str | float]]


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
