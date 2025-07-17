#! /usr/bin/env -S uv run --no-project --with numpy --with textual --with textual-plotext --python 3.13 python
from pathlib import Path

from point_operations_training.model.assignment_model import AssignmentModel
from point_operations_training.presenter.assignment_presenter import AssignmentPresenter
from point_operations_training.view.textual_view import TextualView

# from point_operations_training.tui import LearnArithmetics

if __name__ == "__main__":
    view = TextualView()
    model = AssignmentModel(Path("db.json"))
    app = AssignmentPresenter(view, model)
    app.run()
