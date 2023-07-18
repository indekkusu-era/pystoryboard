from dataclasses import dataclass
import py_midicsv as pm
from enum import Enum

@dataclass
class PitchEvent:
    track_num: int
    beat: float
    pitch: int
    timestamp: float = None
    end: float = None
    note_off: bool = True

@dataclass
class TimeSignatureEvent: 
    beat: float
    numerator: int
    denominator: int
    timestamp: float = None

@dataclass
class TempoEvent:
    beat: float
    microseconds_per_beat: int
    timestamp: float = None

    @property
    def bpm(self) -> float:
        return 6e7 / self.microseconds_per_beat
    
    @property
    def milliseconds_per_beat(self) -> float:
        return self.microseconds_per_beat / 1000

def is_note_off(note_on_event_attributes):
    return int(note_on_event_attributes[-1]) == 0

def _get_midi_event(midifp: str):
    csv = pm.midi_to_csv(midifp, strict=False)
    ticks = None
    for event in csv:
        attributes = event.replace("\n", "").split(", ")
        track_num, time, event_type = attributes[:3]
        track_num = int(track_num)
        event_type = event_type.lower()
        # Header contains tick
        if event_type == 'header':
            ticks = int(attributes[-1])
            continue
        beat = int(time) / ticks
        match event_type:
            case 'tempo':
                microsec_per_beat = int(attributes[-1])
                yield TempoEvent(beat=beat, microseconds_per_beat=microsec_per_beat)
            case 'time_signature':
                num, denom = int(attributes[3]), 2 ** int(attributes[4])
                yield TimeSignatureEvent(beat=beat, numerator=num, denominator=denom)
            case 'note_on_c':
                pitch = int(attributes[-2])
                note_off = is_note_off(attributes)
                yield PitchEvent(track_num=track_num, beat=beat, pitch=pitch, note_off=note_off)

def parse_midi(midifp: str):
    events = _get_midi_event(midifp)
    current_tempo = TempoEvent(0,0,0)
    current_tempo_timestamp = 0
    notes_enabled = []
    for event in events:
        event_timestamp = current_tempo_timestamp + (event.beat - current_tempo.beat) * current_tempo.milliseconds_per_beat
        if isinstance(event, TempoEvent):
            current_tempo = event
            event.timestamp = event_timestamp
            current_tempo_timestamp = event_timestamp
            yield event
        if isinstance(event, PitchEvent):
            event.timestamp = event_timestamp
            if event.note_off:
                track_num = event.track_num; pitch = event.pitch
                idx = next(filter(lambda i: notes_enabled[i].track_num == track_num and notes_enabled[i].pitch == pitch, range(len(notes_enabled))), None)
                if idx is None:
                    continue
                note_event = notes_enabled.pop(idx)
                note_event.end = event.timestamp
                yield note_event
            else:
                notes_enabled.append(event)
        if isinstance(event, TimeSignatureEvent):
            event.timestamp = event_timestamp
            yield event

if __name__ == "__main__":
    events = parse_midi("C://Users/HP/Downloads/among_the_constellation_rh.mid")
    for event in events:
        print(event)
