from numpy import float16
from typing import Type, Iterable
from ..events import Event
from ..events.event_classes import Vector
from ..enums import Layers, Alignment, AnimationLoopType

class Animation:
    def __init__(self, directory_path: str, frame_count: int, frame_delay: int, loop_type=AnimationLoopType.LOOP_FOREVER, 
                 layer=Layers.BACKGROUND, origin=Alignment.CENTRE, xy=Vector(320, 240)):
        self.directory_path = directory_path
        self.frame_count = frame_count
        self.frame_delay = frame_delay
        self.loop_type = loop_type
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
        sprite_data = f'Animation,{self.layer.value},{self.origin},"{self.directory_path}",{str(self.xy)[1:-1].replace(" ", "")},{self.frame_count},{self.frame_delay},{self.loop_type.value}\n '
        event_data = "\n ".join(
            "\n ".join((event.render(precision) for event in event_generator())) for event_generator in self.list_event_generators
        )
        text = sprite_data + event_data
        return text + "\n"

    def __repr__(self):
        return f"Animation(directory: {self.directory_path}, frame_count: {self.frame_count}, layer: {self.layer.name}, origin: {self.origin})"

def create_animation(directory):
    ...
