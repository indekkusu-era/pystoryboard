from dataclasses import dataclass
from pydantic import validate_arguments

@validate_arguments
@dataclass
class TimeRange:
    start: int
    end: int

    def offset(self, offset: int):
        self.start += offset
        self.end += offset

    def render(self):
        if self.start == self.end:
            return f"{self.start},"
        return f"{self.start},{self.end}"
    
    def __repr__(self):
        return f"start: {self.start}, end: {self.end}"

def make_event_value(class_name: type):
    assert hasattr(class_name, 'render'), f'{class_name.__class__.__name__} as no attribute \'render\''
    @dataclass(frozen=True)
    class StartEnd:
        start_value: class_name
        end_value: class_name

        def render(self):
            if self.start_value == self.end_value:
                return self.start_value.render()
            return f"{self.start_value.render()},{self.end_value.render()}"
        
        def __repr__(self):
            if self.start_value == self.end_value:
                return self.start_value.__repr__()
            return f"{self.start_value.__repr__()} -> {self.end_value.__repr__()}"

    return StartEnd

__all__ = ['TimeRange', 'make_event_value']
