from typing import Iterable
from copy import deepcopy as copy
from ..objects.sprite import Sprite
from ..events import Event, LoopEvent
from ..objects import Sprite
from ..enums import Layers

class StoryBoard:
    EVENT_TEXT = "[Events]\n//Background and Video events\n"
    BACKGROUND_TEXT = "//Storyboard Layer 0 (Background)\n"
    FAIL_TEXT = "//Storyboard Layer 1 (Fail)\n"
    PASS_TEXT = "//Storyboard Layer 2 (Pass)\n"
    FOREGROUND_TEXT = "//Storyboard Layer 3 (Foreground)\n"
    OVERLAY_TEXT = "//Storyboard Layer 4 (Overlay)\n"
    SOUND_SAMPLES = "//Storyboard Sound Samples"

    def __init__(self, objects: Iterable[Sprite]) -> None:
        self.objects = objects

    def render(self):
        for object in self.objects:
            match object.layer:
                case Layers.BACKGROUND:
                    ...
                case Layers.FAIL:
                    ...
                case Layers.PASS:
                    ...
                case Layers.FOREGROUND:
                    ...
                case Layers.OVERLAY:
                    ...
        return ""
    
    def render_to_osb(self, osb_file: str):
        ...
