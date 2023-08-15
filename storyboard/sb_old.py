# deprecated, saving for reference in the future

from copy import deepcopy as copy
from ..objects.sprite import Sprite, Position
from ..events.events import Loop, Event
# from ..utils.position_converter import PositionConfig

DEFAULT_PATH = ""

class StoryBoard:
    EVENT_TEXT = "[Events]\n//Background and Video events\n"
    BACKGROUND_TEXT = "//Storyboard Layer 0 (Background)\n"
    FAILPASS_TEXT = "//Storyboard Layer 1 (Fail)\n//Storyboard Layer 2 (Pass)\n"
    FOREGROUND_TEXT = "//Storyboard Layer 3 (Foreground)\n"
    OVERLAY_TEXT = "//Storyboard Layer 4 (Overlay)\n"
    SOUND_SAMPLES = "//Storyboard Sound Samples"

    Objects = {
        'background': [],
        'foreground': [],
        'overlay': []
    }

    def __init__(self, background_objects=None, foreground_objects=None, overlay_objects=None) -> None:
        if not background_objects:
            background_objects = list()
        if not foreground_objects: 
            foreground_objects = list()
        if not overlay_objects:
            overlay_objects = list()
        self.Objects['background'] = background_objects
        self.Objects['foreground'] = foreground_objects
        self.Objects['overlay'] = overlay_objects
    

    def render(self):
        text = self.EVENT_TEXT + \
        self.BACKGROUND_TEXT + "".join([i.render(Position.BACKGROUND) for i in self.Objects['background']]) + \
        self.FAILPASS_TEXT + self.FOREGROUND_TEXT + "".join([i.render(Position.FOREGROUND) for i in self.Objects['foreground']]) + \
        self.OVERLAY_TEXT + "".join([i.render(Position.OVERLAY) for i in self.Objects['overlay']])
        return text + self.SOUND_SAMPLES

    @staticmethod
    def is_sprite(text):
        return "Sprite" in text
    
    @staticmethod
    def is_loop_event(text):
        return "L" in text
    
    @staticmethod
    def is_in_loop_event(text):
        return "  " in text
    
    @staticmethod
    def is_event(text):
        return text[0] == " "
    
    def optimize(self):
        for key in self.Objects.keys():
            self.Objects[key] = self._optimize(self.Objects[key])        

    @staticmethod
    def parse_sprite(sprite_text: str):
        sprite_details = sprite_text.split(",")
        sprite_alignment = sprite_details[2]
        sprite_filename = sprite_details[3][1:-1]
        return Sprite(sprite_filename, sprite_alignment)

    @staticmethod
    def parse_event(event_text: str):
        event_text = event_text.replace(" ", "")
        event_details = event_text.split(",")
        event_type = event_details[0]
        event_easing = int(event_details[1])
        event_start = int(event_details[2])
        if event_details[3]:
            event_end = int(event_details[3])
        else:
            event_end = event_start
        event_params = []
        for dt in event_details[4:]:
            try:
                event_params.append(int(dt))
            except:
                try:
                    event_params.append(float(dt))
                except:
                    event_params.append(dt)

            
        return Event(event_type, event_easing, event_start, event_end, event_params)

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

            if currently_in_loop and (not self.is_in_loop_event(line)):
                current_sprite.add_event(copy(current_loop))
                currently_in_loop = False
            
            if self.is_sprite(line):
                if current_sprite is not None:
                    if current_line == Position.BACKGROUND:
                        self.Objects['background'].append(copy(current_sprite))
                    elif current_line == Position.FOREGROUND:
                        self.Objects['foreground'].append(copy(current_sprite))
                    elif current_line == Position.OVERLAY:
                        self.Objects['overlay'].append(copy(current_sprite))

                current_sprite = self.parse_sprite(line)
                continue
            
            if self.is_loop_event(line):
                current_loop = self.parse_loop(line)
                currently_in_loop = True
                continue

            if currently_in_loop:
                current_loop.events.append(self.parse_event(line))
                continue

            if self.is_event(line):
                current_sprite.add_event(self.parse_event(line))

        osb.close()
        return self
    
    def merge(self, sb2):
        t = copy(self)
        for key in ['background', 'foreground', 'overlay']:
            t.Objects[key] += sb2.Objects[key]
        return t
    
    def add_sprite(self, position: str, sprite: Sprite):
        assert position.lower() in ["background", "foreground", "overlay"]
        if position.lower() == "background":
            self.Objects['background'].append(sprite)
        elif position.lower() == "foreground":
            self.Objects['foreground'].append(sprite)
        elif position.lower() == "overlay":
            self.Objects['overlay'].append(sprite)

    def change_offset(self, offset: int):
        for k in self.Objects.keys():
            for i in range(len(self.Objects[k])):
                self.Objects[k][i].change_offset(offset)

    def osb(self, osb_fp):
        with open(osb_fp, 'w+') as osb:
            osb.write(self.render())

def merge_sb(f1, f2):
    sb1 = StoryBoard().from_osb(f1)
    sb2 = StoryBoard().from_osb(f2)

    return sb1.merge(sb2)
