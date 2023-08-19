from typing import Iterable
from copy import deepcopy
from ..objects.sprite import Sprite
from ..objects import Sprite
from ..enums import StoryboardText

class Storyboard:
    def __init__(self, objects: Iterable[Sprite]) -> None:
        self.objects = deepcopy(objects)

    def render(self):
        text_dict = {enum.name: "\n" for enum in StoryboardText}
        for object in self.objects:
            layer = object.layer
            text_dict[layer.name] += object.render()
        render_result = ""
        for key, value in text_dict:
            storyboard_enum = getattr(StoryboardText, key)
            render_result += storyboard_enum.value + value
        return render_result
    
    def render_to_osb(self, osb_file: str):
        with open(osb_file, 'w+', encoding='utf-8') as f:
            f.write(self.render())

    def __repr__(self):
        ...

def load_osb(osb_file: str):
    raise NotImplementedError()

__all__ = ['Storyboard']
