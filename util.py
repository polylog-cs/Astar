import copy
import itertools
import random
import math
from manim import *
from typing import Set

import solarized
from solarized import *


############### GENERATING SOUNDS

def random_click_file():
    return f"audio/click/click_{random.randint(0, 3)}.wav"


def random_pop_file():
    return f"audio/pop/pop_{random.randint(0, 6)}.wav"


def random_whoosh_file():
    return f"audio/whoosh/whoosh_{random.randint(0, 3)}.wav"


whoosh_gain = -8


def random_whoops_file():
    return f"audio/whoops/whoops{random.randint(1, 1)}.mp3"


def random_rubik_file():
    return f"audio/cube/r{random.randint(1, 20)}.wav"


# use as: 
# self.add_sound(random_whoosh_file(), time_offset = 0.15, gain = whoosh_gain)


###############



