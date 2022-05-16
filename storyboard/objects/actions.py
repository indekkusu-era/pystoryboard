from typing import List, Type
class Action:
    def __init__(self, event_type: str, easing: int, start_time: int, end_time: int, params: list) -> None:
        self.event_type = event_type
        self.easing = easing
        self.start_time = int(start_time)
        self.end_time = int(end_time) if end_time != None else ""
        self.params = params
    
    def __repr__(self):
        return self.render()
    
    def change_offset(self, offset: int):
        self.start_time += int(offset)
        if self.end_time != "":
            self.end_time += int(offset)

    def render(self):
        param_text = ""
        for param in self.params:
            param_text += ","
            if isinstance(param, str):
                param_text += param
            elif param != None:
                param_text += param.__repr__()
            else:
                continue
                
        return f"{self.event_type},{self.easing},{self.start_time},{self.end_time}{param_text}"
    
class Scale(Action):
    def __init__(self, easing: int, start_time: int, end_time:int, start_scale: float, end_scale: float) -> None:
        self.start_scale, self.end_scale = start_scale, end_scale
        super().__init__('S', easing, start_time, end_time, [start_scale, end_scale])

class Move(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, pos_start: tuple, pos_end: tuple) -> None:
        self.x_start, self.y_start = pos_start
        self.x_end, self.y_end = pos_end
        super().__init__('M', easing, start_time, end_time, [self.x_start, self.y_start, self.x_end, self.y_end])

class Fade(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, opacity_start: float, opacity_end: float) -> None:
        self.opacity_start = opacity_start
        self.opacity_end = opacity_end
        super().__init__('F', easing, start_time, end_time, [opacity_start, opacity_end])

class Rotate(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, angle_start: float, angle_end: float) -> None:
        self.angle_start = angle_start
        self.angle_end = angle_end
        super().__init__('R', easing, start_time, end_time, [angle_start, angle_end])

class Color(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, RGB1: tuple, RGB2: tuple):
        self.r1, self.g1, self.b1 = RGB1
        self.r2, self.g2, self.b2 = RGB2
        super().__init__('C', easing, start_time, end_time, [self.r1, self.g1, self.b1, self.r2, self.g2, self.b2])

class VectorScale(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, start_size: tuple, end_size: tuple) -> None:
        self.start_x, self.start_y = start_size
        self.end_x, self.end_y = end_size
        super().__init__('V', easing, start_time, end_time, [self.start_x, self.start_y, self.end_x, self.end_y])

class MoveX(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, x_start: float, x_end: float) -> None:
        self.x_start = x_start; self.x_end = x_end
        super().__init__('MX', easing, start_time, end_time, [x_start, x_end])

class MoveY(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, y_start: float, y_end: float) -> None:
        self.y_start = y_start; self.x_end = y_end
        super().__init__('MY', easing, start_time, end_time, [y_start, y_end])

class Loop():
    def __init__(self, start_time: int, loop_count: int, actions: List[Type[Action]]) -> None:
        self.start_time = start_time
        self.loop_count = loop_count
        self.actions = actions
    
    def __repr__(self):
        loop_text = f"L,{self.start_time},{self.loop_count}\n  "
        loop_text += "\n  ".join([action.__repr__() for action in self.actions])
        return loop_text
    
    def render(self):
        return self.__repr__()