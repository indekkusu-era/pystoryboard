from numpy import float16
from typing import Type, Iterable
from ..events import Event
from ..events.event_classes import Vector
from ..enums import Layers, Alignment

class Sprite:
    def __init__(self, file_path: str, layer=Layers.BACKGROUND, origin=Alignment.CENTRE, xy=Vector(320, 240)):
        self.file_path = file_path
        self.layer = layer
        self.origin = origin
        self.xy = xy
        self.list_event_generators = []
    
    def add_event(self, event: Type[Event]):
        def _event_gen():
            yield event
        self.list_event_generators.append(_event_gen())

    def events(self, timestamp: int = 0):
        def add_events(event_generator: Iterable[Type[Event]]):
            def scrolled_events():
                for event in event_generator():
                    yield event.offset(timestamp)
            self.list_event_generators.append(scrolled_events())
        return add_events

    def render(self, precision=float16):
        sprite_data = f'Sprite,{self.layer.value},{self.origin},"{self.file_path}",{str(self.xy)[1:-1].replace(" ", "")}\n '
        event_data = "\n ".join(
            "\n ".join((event.render(precision) for event in event_generator())) for event_generator in self.list_event_generators
        )
        text = sprite_data + event_data
        return text + "\n"
    
    def __repr__(self):
        return f"Sprite(file_path: {self.file_path}, layer: {self.layer.name}, origin: {self.origin})"
