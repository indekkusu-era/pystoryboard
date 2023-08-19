from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Iterable, Type, Generator
from .events import Event
from ..enums import TriggerEvents, CompoundEventType

class CompoundEvent:
    def __init__(self, event_type: CompoundEventType, start_time: int, events: Iterable[Type[Event]]):
        self.event_type = event_type
        self.start_time = start_time
        self.events = deepcopy(events)
    
    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()
    
    @abstractmethod
    def render(self):
        raise NotImplementedError()

class LoopEvent(CompoundEvent):
    def __init__(self, start_time: int, loop_count: int, events: Iterable[Type[Event]]):
        super().__init__(CompoundEventType.LOOP, start_time, events)
        self.loop_count = loop_count
    
    def __repr__(self):
        return f"{self.event_type.name}(start_time: {self.start_time}, loop_count: {self.loop_count})"

    def render(self):
        loop_text = f"{self.event_type.value},{self.start_time},{self.loop_count}\n  "
        loop_text += "\n  ".join((event.render() for event in self.events))
        return loop_text

class TriggerEvent(CompoundEvent):
    def __init__(self, trigger_name: TriggerEvents, start_time: int, end_time: int, events: Iterable[Type[Event]]):
        super().__init__(CompoundEventType.TRIGGER, start_time, events)
        self.trigger_name = trigger_name
        self.end_time = end_time

    def __repr__(self):
        return f"{self.event_type.name}(trigger_type: {self.trigger_name.name}, start_time: {self.start_time}, end_time: {self.end_time})"

    def render(self):
        loop_text = f"{self.event_type.value},{self.trigger_name.value},{self.start_time},{self.end_time}\n  "
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
