from tqdm import tqdm
from typing import Type
from events.event_set import BaseEventSet

class EventQueue:
    def __init__(self, list_events: list[Type[BaseEventSet]]) -> None:
        self.list_events = list_events

    def render(self):
        ...