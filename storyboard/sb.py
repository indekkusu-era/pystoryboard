from copy import deepcopy as copy
from enum import Enum
from typing import List, Optional, Type
from typing_extensions import Literal
from .actions import Action, Loop

DEFAULT_PATH = ""

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

class StoryBoard:
    EVENT_TEXT = "[Events]\n//Background and Video events\n"
    BACKGROUND_TEXT = "//Storyboard Layer 0 (Background)\n"
    FAILPASS_TEXT = "//Storyboard Layer 1 (Fail)\n//Storyboard Layer 2 (Pass)\n"
    FOREGROUND_TEXT = "//Storyboard Layer 3 (Foreground)\n"
    OVERLAY_TEXT = "//Storyboard Layer 4 (Overlay)\n"
    SOUND_SAMPLES = "//Storyboard Sound Samples"
    background_object = []
    foreground_object = []
    overlay_object = []
    def __init__(self, background_objects=[], foreground_objects=[], overlay_objects=[]) -> None:
        self.background_object = background_objects
        self.foreground_object = foreground_objects
        self.overlay_object = overlay_objects
    
    def render(self):
        text = self.EVENT_TEXT + \
        self.BACKGROUND_TEXT + "".join([i.render(Position.BACKGROUND) for i in self.background_object]) + \
        self.FAILPASS_TEXT + self.FOREGROUND_TEXT + "".join([i.render(Position.FOREGROUND) for i in self.foreground_object]) + \
        self.OVERLAY_TEXT + "".join([i.render(Position.OVERLAY) for i in self.overlay_object])
        return text + self.SOUND_SAMPLES

    @staticmethod
    def is_sprite(text):
        return "Sprite" in text
    
    @staticmethod
    def is_loop_action(text):
        return "L" in text
    
    @staticmethod
    def is_in_loop_action(text):
        return "  " in text
    
    @staticmethod
    def is_action(text):
        return text[0] == " "

    @staticmethod
    def parse_sprite(sprite_text: str):
        sprite_details = sprite_text.split(",")
        sprite_type = sprite_details[0]
        sprite_overlay = sprite_details[1]
        sprite_alignment = sprite_details[2]
        sprite_filename = sprite_details[3][1:-1]
        return Sprite(sprite_filename)

    @staticmethod
    def parse_action(action_text: str):
        action_text = action_text.replace(" ", "")
        action_details = action_text.split(",")
        action_type = action_details[0]
        action_easing = int(action_details[1])
        action_start = int(action_details[2])
        if action_details[3]:
            action_end = int(action_details[3])
        else:
            action_end = action_start
        action_params = []
        for dt in action_details[4:]:
            try:
                action_params.append(int(dt))
            except:
                try:
                    action_params.append(float(dt))
                except:
                    action_params.append(dt)

            
        return Action(action_type, action_easing, action_start, action_end, action_params)

    @staticmethod
    def parse_loop(loop_text: str):
        L, start_time, loop_count = loop_text.split(",")
        start_time = int(start_time)
        loop_count = int(loop_count)
        return Loop(start_time, loop_count, [])

    def from_osb(self, osb_fp: str):
        osb = open(osb_fp, 'r', encoding='utf-8')
        osb_text = osb.read().split("\n")
        current_line = -1
        current_sprite = None
        current_loop = None
        currently_in_loop = False
        for line in osb_text:
            if line in self.BACKGROUND_TEXT:
                current_line = Position.BACKGROUND
                continue
            elif line in self.FAILPASS_TEXT:
                current_line = -1
                continue
            elif line in self.FOREGROUND_TEXT:
                current_line = Position.FOREGROUND
                continue
            elif line in self.OVERLAY_TEXT:
                current_line = Position.OVERLAY
                continue

            if currently_in_loop and (not self.is_in_loop_action(line)):
                current_sprite.add_action(copy(current_loop))
                currently_in_loop = False
            
            if self.is_sprite(line):
                if current_sprite is not None:
                    if current_line == Position.BACKGROUND:
                        self.background_object.append(copy(current_sprite))
                    elif current_line == Position.FOREGROUND:
                        self.foreground_object.append(copy(current_sprite))
                    elif current_line == Position.OVERLAY:
                        self.overlay_object.append(copy(current_sprite))

                current_sprite = self.parse_sprite(line)
                continue
            
            if self.is_loop_action(line):
                current_loop = self.parse_loop(line)
                currently_in_loop = True
                continue

            if currently_in_loop:
                current_loop.actions.append(self.parse_action(line))
                continue

            if self.is_action(line):
                current_sprite.add_action(self.parse_action(line))

        osb.close()
        return self
    
    def merge(self, sb2):
        t = copy(self)
        t.background_object += sb2.background_object
        t.foreground_object += sb2.foreground_object
        t.overlay_object += sb2.overlay_object
        return t
    
    def add_sprite(self, position: str, sprite: Sprite):
        assert position.lower() in ["background", "foreground", "overlay"]
        if position.lower() == "background":
            self.background_object.append(sprite)
        elif position.lower() == "foreground":
            self.foreground_object.append(sprite)
        elif position.lower() == "overlay":
            self.overlay_object.append(sprite)

    def osb(self, osb_fp):
        with open(osb_fp, 'w+') as osb:
            osb.write(self.render())

def merge_sb(f1, f2):
    sb1 = StoryBoard().from_osb(f1)
    sb2 = StoryBoard().from_osb(f2)

    return sb1.merge(sb2)