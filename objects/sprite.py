import os
from tqdm import tqdm
from typing import List, Type
from typing_extensions import Literal
from enum import Enum
from PIL import Image
from events import Event
from events.events import PixelScale

class Position(Enum):
    BACKGROUND = 0
    FOREGROUND = 1
    OVERLAY = 2

class ImageNotFoundError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class Sprite:
    def __init__(self, file_name, align='Centre', origin=(320, 240), id=None):
        self.filename = file_name
        self.align = align
        self._id = id
        self._origin = origin
        self.Event = []
    
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

    def add_event(self, Event: Type[Event]):
        self.Event.append(Event)
        return self
    
    def add_events(self, Events: List[Type[Event]]):
        self.Event += Events
        return self
    
    def _render(self, pos, events):
        string = {
            Position.BACKGROUND: "Background",
            Position.FOREGROUND: "Foreground",
            Position.OVERLAY: "Overlay"
        }
        sprite_data = f'Sprite, {string[pos]}, {self.align}, "{self.filename}", {",".join(self._origin)}\n'
        event_render_text = []
        for event in events:
            if isinstance(event, PixelScale):
                if not self.image_size:
                    raise ImageNotFoundError('Found PixelScale in the Sprite, but Image not found')
                event_render_text.append(event.render(self.image_size))
                continue
            event_render_text.append(event.render())
        event_data = "\n".join(event_render_text)
        text = sprite_data + event_data
        return text + "\n"

    def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
        return self._render(pos, self.Event)
        
class ThreeDimensionSprite(Sprite):
    def __init__(self, file_name, align='Centre', origin=(320, 240), id=None):
        super().__init__(file_name, align, origin, id)
