from typing import Iterable, Type, Generator
from .events import Event
from ..enums import TriggerEvents

class LoopEvent:
    def __init__(self, start_time: int, loop_count: int, events: Iterable[Type[Event]]):
        self.start_time = start_time
        self.loop_count = loop_count
        self.events = events
    
    def __repr__(self):
        return f"Loop(start_time: {self.start_time}, loop_count: {self.loop_count})"

    def render(self):
        loop_text = f"L,{self.start_time},{self.loop_count}\n  "
        loop_text += "\n  ".join((event.render() for event in self.events))
        return loop_text

class TriggerEvent:
    def __init__(self, trigger_name: TriggerEvents, start_time: int, end_time: int, events: Iterable[Type[Event]]):
        self.trigger_name = trigger_name
        self.start_time = start_time
        self.end_time = end_time
        self.events = events

    def __repr__(self):
        return f"Trigger(trigger_type: {self.trigger_name.name}, start_time: {self.start_time}, end_time: {self.end_time})"

    def render(self):
        loop_text = f"T,{self.trigger_name.value},{self.start_time},{self.end_time}\n  "
        loop_text += "\n  ".join((event.render() for event in self.events))
        return loop_text

class Loop:
    def __init__(self, start_time: int, loop_count: int):
        self.start_time = start_time
        self.loop_count = loop_count
    
    def __call__(self, event_generator: Generator):
        return LoopEvent(self.start_time, self.loop_count, event_generator())

class Trigger:
    def __init__(self, trigger_name: TriggerEvents, start_time: int, end_time: int):
        self.trigger_name = trigger_name
        self.start_time = start_time
        self.end_time = end_time
    
    def __call__(self, event_generator: Generator):
        return TriggerEvent(self.trigger_name, self.start_time, self.end_time, event_generator())

__all__ = ['LoopEvent', 'TriggerEvent', 'Loop', 'Trigger']
