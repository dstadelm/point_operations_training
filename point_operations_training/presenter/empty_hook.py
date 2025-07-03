from typing import Callable


def create_empty_event_hook(event_hook_name: str) -> Callable[[], None]:
    def dummy_event_hook() -> None:
        """A dummy event hook to avoid NotImplementedError."""
        raise NotImplementedError(f"Missing {event_hook_name} event hook.")

    return dummy_event_hook
