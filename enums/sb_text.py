from enum import Enum

class StoryboardText(Enum):
    EVENT = "[Events]\n//Background and Video events\n"
    BACKGROUND = "//Storyboard Layer 0 (Background)\n"
    FAIL = "//Storyboard Layer 1 (Fail)\n"
    PASS = "//Storyboard Layer 2 (Pass)\n"
    FOREGROUND = "//Storyboard Layer 3 (Foreground)\n"
    OVERLAY = "//Storyboard Layer 4 (Overlay)\n"
    SOUND_SAMPLES = "//Storyboard Sound Samples"

__all__ = ['StoryboardText']
