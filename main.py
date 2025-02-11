#!/usr/bin/env python3
from point_operations_training.tui import LearnArithmetics


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
