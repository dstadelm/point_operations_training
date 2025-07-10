import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Timer:
    DEBUG: bool = False

    def __init__(self, name: str):
        self.name: str = name
        self.start_time: float = time.time()
        self.stop_time: float = time.time()

    def start(self):
        self.start_time = time.time()

    def stop(self) -> None:
        self.stop_time = time.time()

    def duration(self) -> float:
        duration = self.stop_time - self.start_time
        return duration
