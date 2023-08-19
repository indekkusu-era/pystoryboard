from enum import Enum

class TriggerEvents(Enum):
    HITSOUND_CLAP = 'HitSoundClap'
    HITSOUND_FINISH = 'HitSoundFinish'
    HITSOUND_WHISTLE = 'HitSoundWhistle'
    PASSING = 'Passing'
    FAILING = 'Failing'

__all__ = ['TriggerEvents']
