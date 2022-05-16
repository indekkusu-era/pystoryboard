from typing import List, Type
from typing_extensions import Literal
from enum import Enum
from .actions import Action

class Position(Enum):
    BACKGROUND = 0
    FOREGROUND = 1
    OVERLAY = 2

class Sprite:
    def __init__(self, file_name):
        self.filename = file_name
        self.action = []
    
    def add_action(self, action: Type[Action]):
        self.action.append(action)
    
    def add_actions(self, actions: List[Type[Action]]):
        self.action += actions
    
    def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
        string = {
            Position.BACKGROUND: "Background",
            Position.FOREGROUND: "Foreground",
            Position.OVERLAY: "Overlay"
        }
        text = f'Sprite,{string[pos]},Centre,"{self.filename}",320,240\n ' + "\n ".join([i.render() for i in self.action])
        return text + "\n"

# class SpriteGroup:
#     def __init__(self) -> None:
#         self.sprites: dict = {}
#         self.actions = []

#     def add_sprite(self, sprite_id, sprite, child_position: tuple):
#         self.sprites[sprite_id] = {
#             'sprite': sprite,
#             'child_position': child_position
#         }
    
#     def add_action(self, action: Type[Action]):
#         self.actions.append(action)
    
#     def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
#         for sprite_id, sprite_data in self.sprites.items():
#             sprite = sprite_data['sprite']
#             child_x, child_y = sprite_data['child_position']
#             for action in self.actions:
#                 pass

#     def __getitem__(self, key):
#         return self.sprites.get(key)