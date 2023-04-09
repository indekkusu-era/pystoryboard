from typing_extensions import Literal
from .sprite import Position, Sprite

class Animation(Sprite):
    def __init__(self, folder_name, align='Centre', origin=(320, 240), id=None):
        super.__init__(self, folder_name, align, origin, id)
    
    def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
        string = {
            Position.BACKGROUND: "Background",
            Position.FOREGROUND: "Foreground",
            Position.OVERLAY: "Overlay"
        }
        text = f'Animation,{string[pos]},{self.align},"{self.filename}",{",".join(self._origin)}\n ' + "\n ".join([i.render() for i in self.Event])
        return text + "\n"
