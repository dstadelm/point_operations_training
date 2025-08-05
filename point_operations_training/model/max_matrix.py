from point_operations_training.model.assignment import AssignmentCollection

MaxMatrixType = dict[str, float]


class MaxMatrix:
    def __init__(self) -> None:
        self.matrix: MaxMatrixType = {}
        self._list: list[tuple[int, ...]] = []

    @property
    def sorted_list(self) -> list[tuple[int, ...]]:
        """Returns a list of the worst assignments sorted from slowest to fastest."""
        if not self._list:
            self._list = self.get_worst_n()
        return self._list

    def update_list(self) -> None:
        """Updates the sorted list of worst assignments."""
        self._list = self.get_worst_n()

    def tuple2key(self, t: tuple[int, int, int]) -> str:
        return f"{t[0]},{t[1]}"

    def key2tuple(self, key: str) -> tuple[int, ...]:
        return tuple([int(x) for x in key.split(",")])

    def update(self, assignements: AssignmentCollection) -> None:
        for assignment in assignements.assignments:
            current_value = self.matrix.setdefault(
                self.tuple2key(assignment.assignment), 0
            )
            new_value = (
                assignment.solve_time
                if assignment.solve_time > current_value
                else current_value
            )
            self.matrix[self.tuple2key(assignment.assignment)] = new_value

        self.update_list()

    def sort_by_value(self) -> None:
        self.matrix = dict(reversed(sorted(self.matrix.items(), key=lambda x: x[1])))

    def get_worst_n_percent(self, percentage: int) -> list[tuple[int, ...]]:
        self.sort_by_value()
        num_values = int(len(self.matrix) * percentage / 100)
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]

    def get_worst_n(self, num_values: int | None = None) -> list[tuple[int, ...]]:
        """Returns a list of n values sorted from slowest to fastest.

        If num_values is None, it returns all values.
        """
        self.sort_by_value()
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]

    def __getitem__(self, idx: int) -> tuple[int, ...]:
        return self.sorted_list[idx]

    def __len__(self) -> int:
        return len(self.sorted_list)
