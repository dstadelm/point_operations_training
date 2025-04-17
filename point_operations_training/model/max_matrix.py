from point_operations_training.model.session import Session

MaxMatrixType = dict[str, float]


class MaxMatrix:
    def __init__(self) -> None:
        self.matrix: MaxMatrixType = {}

    def tuple2key(self, t: tuple[int, int]) -> str:
        return f"{t[0]},{t[1]}"

    def key2tuple(self, key: str) -> tuple[int, ...]:
        return tuple([int(x) for x in key.split(",")])

    def update(self, session: Session) -> None:
        for assignment in session:
            current_value = self.matrix.setdefault(
                self.tuple2key(assignment.assignment), 0
            )
            new_value = (
                assignment.solve_time
                if assignment.solve_time > current_value
                else current_value
            )
            self.matrix[self.tuple2key(assignment.assignment)] = new_value

    def sort_by_value(self) -> None:
        self.matrix = dict(reversed(sorted(self.matrix.items(), key=lambda x: x[1])))

    def get_worst_n_percent(self, percentage: int) -> list[tuple[int, ...]]:
        self.sort_by_value()
        num_values = int(len(self.matrix) * percentage / 100)
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]

    def get_worst_n(self, num_values: int) -> list[tuple[int, ...]]:
        self.sort_by_value()
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]
