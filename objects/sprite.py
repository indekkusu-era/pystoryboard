import os
from typing import Type, Iterable
from typing_extensions import Literal
from PIL import Image
from ..events import Event
from ..enums import Layers
from pipe import traverse

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
        return event.render()

    def _render(self, pos, events: list[Type[Event]]):
        string = {
            Layers.BACKGROUND: "Background",
            Layers.FOREGROUND: "Foreground",
            Layers.OVERLAY: "Overlay"
        }
        sprite_data = f'Sprite,{string[pos]},{self.align},"{self.filename}",{str(self._origin)[1:-1].replace(" ", "")}\n '
        event_render_text = []
        for event in events:
            event_render_text.append(event.render())
        
        event_data = "\n ".join(event_render_text | traverse)
        text = sprite_data + event_data
        return text + "\n"

    def render(self, pos: Literal[Layers.BACKGROUND, Layers.FOREGROUND, Layers.OVERLAY]):
        return self._render(pos, self.events)
