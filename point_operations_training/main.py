#! /usr/bin/env -S uv run --no-project --with numpy --with textual --with textual-plotext --python 3.13 python
from point_operations_training.presenter.presenter import AssignmentPresenter
from point_operations_training.view.view import TextualView

# from point_operations_training.tui import LearnArithmetics

if __name__ == "__main__":
    view = TextualView()
    app = AssignmentPresenter(view)
    app.run()
