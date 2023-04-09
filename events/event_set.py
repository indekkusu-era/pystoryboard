from abc import ABC, abstractmethod
from .events import Event, Move
from midiparser import parse_midi
from midiparser.parser import PitchEvent, TimeSignatureEvent, TempoEvent
from random import uniform
from objects import Sprite, Animation

class BaseEventSet(ABC):
    def __init__(self, gen_event_function):
        self._gen_event_function = gen_event_function
    
    @abstractmethod
    def render(self) -> list[Sprite]:
        ...

class EventSet(BaseEventSet):
    def __init__(self, gen_event_function):
        super().__init__(self, gen_event_function)

    @property
    def ms(self):
        return int(1000 / self._fps)
    
    def render(self, start, end, fps=24):
        self._fps = fps
        t = start
        all_sprites = []
        while t < end:
            all_sprites.extend(self._gen_event_function(start, t, end))
            t += self.ms

class TimeStampEventSet(BaseEventSet):
    def __init__(self, gen_event_function):
        super().__init__(self, gen_event_function)
    
    def render(self, timestamps):
        all_sprites = []
        for t in timestamps:
            all_sprites.extend(self._gen_event_function(t))
        return all_sprites

class MIDIEventSet(TimeStampEventSet):
    def __init__(self, gen_event_function):
        super().__init__(self, gen_event_function)
    
    def render(self, midi_file):
        events = parse_midi(midi_file)
        all_sprites = []
        for event in events:
            if isinstance(event, PitchEvent):
                all_sprites.extend(self._gen_event_function(pitch=event))
            if isinstance(event, TimeSignatureEvent):
                all_sprites.extend(self._gen_event_function(time_signature=event))
            if isinstance(event, TempoEvent):
                all_sprites.extend(self._gen_event_function(tempo=event))
        return all_sprites

if __name__ == "__main__":
    @TimeStampEventSet
    def Rain(t: int):
        rain = Sprite('rain.png')
        rng = uniform(0, 640)
        rain.add_event(Move(0, t, t+1000, (rng, 0), (rng, 480)))
        yield rain

    Rain.render([10,20,30])
