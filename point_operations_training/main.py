#! /usr/bin/env -S uv run --no-project --with numpy --with textual --with textual-plotext --python 3.13 python
from point_operations_training.presenter.presenter import Presenter
from point_operations_training.view.view import UserView

# from point_operations_training.tui import LearnArithmetics

if __name__ == "__main__":
    view = UserView()
    app = Presenter(view)
    app.run()
