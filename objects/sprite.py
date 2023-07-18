import os
from tqdm import tqdm
from typing import Type, Iterable
from typing_extensions import Literal
from enum import Enum
from PIL import Image
from events import Event
from pipe import traverse

class Position(Enum):
    BACKGROUND = 0
    FOREGROUND = 1
    OVERLAY = 2

class ImageNotFoundError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class Sprite:
    def __init__(self, file_name, align='Centre', origin=(320, 240)):
        self.filename = file_name
        self.align = align
        self._origin = origin
        self.events = list()
    
    def from_image(self, image_content: Image):
        if os.path.isfile(self.filename):
            return self
        image_content.save(self.filename)
        return self
    
    @property
    def image_size(self):
        if not os.path.isfile(self.filename):
            return
        return Image.open(self.filename).size

    def add_event(self, event: Type[Event]):
        self.events.append(event)
        return self
    
    def add_events(self, events: Iterable[Type[Event]]):
        self.events.extend(events)
        return self
    
    def render_event(self, event: Type[Event]):
        kwargs = {
            'image_size': self.image_size,
        }

        return event.render(**kwargs)

    def _render(self, pos, events: list[Type[Event]]):
        string = {
            Position.BACKGROUND: "Background",
            Position.FOREGROUND: "Foreground",
            Position.OVERLAY: "Overlay"
        }
        sprite_data = f'Sprite,{string[pos]},{self.align},"{self.filename}",{str(self._origin)[1:-1]}\n '
        event_render_text = []
        for event in events:
            event_render_text.append(self.render_event(event))
        
        event_data = "\n ".join(event_render_text | traverse)
        text = sprite_data + event_data
        return text + "\n"

    def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
        return self._render(pos, self.events)
