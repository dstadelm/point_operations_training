from enum import Enum

from point_operations_training.model.assignment import (
    DivisionAssignmentFactory,
    MultiplicationAssignmentFactory,
    TensMultiplicationAssignmentFactory,
)


class Modus(Enum):
    MULTIPLICATION = MultiplicationAssignmentFactory()
    MULTIPLICATIONx10 = TensMultiplicationAssignmentFactory()
    DIVISION = DivisionAssignmentFactory()
