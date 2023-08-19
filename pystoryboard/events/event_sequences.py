import numpy as np
from numpy import float16
from math import ceil
from ..enums import Easing, EventType
from .event_classes import Scalar
from .event_classes import IntegerSequence

"""
# Usage

@EventSequence('M', start, end, frame_rate=24, easing=LINEAR)
def value_generator(t: float 0-1):
    return value(t)

# Usage with sprite

sprite = Sprite('sample.png')

@sprite.events(timestamp=12345)
@EventSequence('M', start, end, frame_rate=24, easing=LINEAR)
def value_generator(t: float 0-1):
    return value(t)
"""

def _scalar_wrapper(f):
    for i in f():
        yield Scalar(i)

class EventSequence:
    def __init__(self, event_type: EventType, start: int, end: int, sequence_type=IntegerSequence, frame_rate=24, easing=Easing.LINEAR):
        self.event_type = event_type
        self.start = start
        self.end = end
        self.frame_rate = frame_rate
        self.easing = easing
        self.sequence_type=sequence_type

    @property
    def ms_per_frame(self):
        return 1000 // self.frame_rate
    
    @property
    def n_samples(self):
        return int(ceil(((self.end - self.start) / self.ms_per_frame)))
    
    def __repr__(self):
        ...

    def __call__(self, f):
        event_type = self.event_type
        start = self.start
        end = self.end
        frame_rate = self.frame_rate
        easing = self.easing

        class AnonymousEventGenerator(EventSequence):
            def __init__(self):
                super().__init__(event_type, start, end, frame_rate, easing)
                self.f = f
            
            @property
            def sequence(self):
                return self.sequence_type(np.vectorize(f), self.n_samples)

            def render(self, precision=float16):
                return f'{self.event_type.value},{self.easing.value},{self.start},{self.start+self.ms_per_frame},{self.sequence.render(precision)}'
            
            def __iter__(self):
                self.activated = False
                return self

            def __next__(self):
                if self.activated:
                    del self.activated
                    raise StopIteration
                self.activated = True
                return self
        
        return AnonymousEventGenerator

class ScalarSequenceEvent(EventSequence):
    def __init__(self, event_type: EventType, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)
    
    def __call__(self, f):
        return super().__call__(_scalar_wrapper(f))

class VectorSequenceEvent(EventSequence):
    def __init__(self, event_type: EventType, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)

class ColorSequenceEvent(EventSequence):
    def __init__(self, event_type: EventType, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)

class ScaleSequence(ScalarSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.SCALE, start, end, frame_rate, easing)

class MoveSequence(VectorSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.MOVE, start, end, frame_rate, easing)

class FadeSequence(ScalarSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.FADE, start, end, frame_rate, easing)

class RotateSequence(ScalarSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.ROTATE, start, end, frame_rate, easing)

class ColorSequence(ColorSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.COLOR, start, end, frame_rate, easing)

class VectorScaleSequence(VectorSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.VECTORSCALE, start, end, frame_rate, easing)

class MoveXSequence(ScalarSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.MOVEX, start, end, frame_rate, easing)

class MoveYSequence(ScalarSequenceEvent):
    def __init__(self, start: int, end: int, frame_rate=24, easing=Easing.LINEAR):
        super().__init__(EventType.MOVEY, start, end, frame_rate, easing)

__all__ = ['ScaleSequence', 'MoveSequence', 'FadeSequence', 'RotateSequence', 'ColorSequence', 'VectorScaleSequence', 'MoveXSequence', 'MoveYSequence']
