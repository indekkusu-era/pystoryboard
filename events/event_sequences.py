import numpy as np
from math import ceil
from ..enums import Easing, EventType
from .event_classes import Scalar

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
    def __init__(self, event_type: EventType, start: int, end: int, frame_rate=None, easing=Easing.LINEAR):
        self.event_type = event_type
        self.start = start
        self.end = end
        self.frame_rate = frame_rate if frame_rate else 24
        self.easing = easing

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

            def render(self):
                samples = np.vectorize(f)(np.linspace(0, 1, self.n_samples))
                render_text = ",".join((x.render() for x in samples))
                return f'{self.event_type.value},{self.easing.value},{self.start},{self.start+self.ms_per_frame},{render_text}'
            
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

class ScalarSequence(EventSequence):
    def __init__(self, event_type: EventType, start=None, end=None, frame_rate=None, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)
    
    def __call__(self, f):
        return super().__call__(_scalar_wrapper(f))

class VectorSequence(EventSequence):
    def __init__(self, event_type: EventType, start=None, end=None, frame_rate=None, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)

class ColorSequence(EventSequence):
    def __init__(self, event_type: EventType, start=None, end=None, frame_rate=None, easing=Easing.LINEAR):
        super().__init__(event_type, start, end, frame_rate, easing)

__all__ = []
