# Storyboard Module by IndexError : Documentation

This module is for storyboard coding in python

---

## Storyboard Objects

Currently there is a support for Sprite only, please wait for a developer to not be lazy to add animations
You can create a Sprite by 

```python {all|2|1-6|9|all}
from storyboard import Sprite

# Create a Sprite for sample.png
my_sprite = Sprite('sample.png')
```

## Adding Actions to Sprite

The action will be in the `.actions` module, it will create effects to the storyboard

```python {all|2|1-6|9|all}
from storyboard import Sprite
from storyboard.actions import Scale

# Create a Sprite for sample.png
my_sprite = Sprite('sample.png')
# Add Scale 1.0 Action from 0ms to 1000ms
# Scale(easing, start_ms, end_ms, start_scale, end_scale)
my_sprite.add_action(Scale(0, 0, 1000, 1.0, 1.0))
```

## Rendering a Storyboard

After finishing do animations to all objects, the next job is to render, you can render by using `Storyboard` class

```python {all|2|1-6|9|all}
from storyboard import Sprite, Storyboard
from storyboard.actions import Scale

my_sprite = Sprite('sample.png')
my_sprite.add_action(Scale(0, 0, 1000, 1.0, 1.0))

# assign objects into storyboard
sb = Storyboard(background_objects=[my_sprite])
# render to .osb
sb.osb('example.osb')
```

---

## Loop Action

`Loop` Action is a special kind of action that will loop for a given times, for example

```python {all|2|1-6|9|all}
from storyboard import Sprite, Storyboard
from storyboard.actions import Fade, Loop

my_sprite = Sprite('sample.png')
# Define the list of actions to loop
fade_in_fade_out = [Fade(0, 0, 500, 0, 1), Fade(0, 500, 1000, 1, 0)]
# Loop fade in -> fade out 10 times, start at 0 ms
loop_fade_in_out = Loop(0, 10, fade_in_fade_out)
# Add the loop into the Sprite
my_sprite.add_action(loop_fade_in_out)

# render to storyboard
sb = Storyboard(background_objects=[my_sprite])
sb.osb('example.osb')
```

## Custom Action

You can create your own action based on the class `Action`, here is the example

```python {all|2|1-6|9|all}
from storyboard.actions import Action

# Create your own 'ScaleUp' Action
class ScaleUp(Action):
    def __init__(self, start, end):
        # This action works like Scale from 0 to 1
        super().__init__('S', 0, start, end, [0, 1])

my_sprite = Sprite('sample.png')
# You can add the action you created to your own sprite
my_sprite.add_action(ScaleUp(0, 1000))
```

## Custom Render Function

TBA

---

## Image Generation

TBA

---

## Storyboard Parsing & Appending

You can parse the storyboard from the .osb file by using `Storyboard().from_osb(file_path)`

```python {all|2|1-6|9|all}
from storyboard import Storyboard

osb_fp = 'M2U - Yoake no Uta (feat. DAZBEE) (SurfChu85).osb'

# parse the storyboard from osb_file
sb = Storyboard().from_osb(osb_fp)

# copy it into the new storyboard
sb.osb('totally-not-copied-storyboard.osb')
```

## Merging Storyboards

Merging Storyboard feature is for the collaborative storyboarding, you can merge the storyboard by using `Storyboard.merge`

```python {all|2|1-6|9|all}
from storyboard import Storyboard

# parse sb1.osb
sb1 = Storyboard().from_osb('sb1.osb')
# parse sb2.osb
sb2 = Storyboard().from_osb('sb2.osb')

# merge storyboard
merged_sb = sb1.merge(sb2)

# render into a new file
merged_sb.osb('merged_storyboard.osb')
```

Or you can use `merge_sb` function

```python {all|2|1-6|9|all}
from storyboard import merge_sb

# merge sb1.osb and sb2.osb together
merged_sb = merge_sb('sb1.osb', 'sb2.osb')

# render it into a new file
merged_sb.osb('merged_storyboard.osb')
```