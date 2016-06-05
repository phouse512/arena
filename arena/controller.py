import enum
import os
import time


@enum.unique
class Button(enum.Enum):
    A = 'a'
    B = 'b'
    X = 'x'
    Y = 'y'
    Z = 'z'
    START = 'start' 
    L = 'l'
    R = 'r'
    D_UP = 'd_up'
    D_DOWN = 'd_down'
    D_LEFT = 'd_left'
    D_RIGHT = 'd_right'


@enum.unique
class Trigger(enum.Enum):
    L = 'l'
    R = 'r'


@enum.unique
class Stick(enum.Enum):
    MAIN = 'main'
    C = 'c'


@enum.unique
class Direction(enum.Enum):
    UP = (.5, 1)
    DOWN = (.5, 0)
    LEFT = (0, .5)
    RIGHT = (1, .5)
    UP_LEFT = (0, 1)
    UP_RIGHT = (1, 1)
    DOWN_LEFT = (0, 0)
    DOWN_RIGHT = (1, 0)
    NEUTRAL = (.5, .5)


class Controller:
    """ Writes controller inputs to pipe """

    def __init__(self, path):
        """ opens the fifo """
        self.pipe = None
        try:
            os.mkfifo(path)
        except OSError:
            print "failure"
            pass
        self.pipe = open(path, 'w', buffering=1)

    def __del__(self):
        if self.pipe:
            self.pipe.close()

    def _press_button(self, button):
        """ press a button, here button is the Button enum """
        assert button in Button
        self.pipe.write('PRESS {}\n'.format(button.name))

    def _release_button(self, button):
        """ release button, button is the Button enum """
        assert button in Button
        self.pipe.write('RELEASE {}\n'.format(button.name))

    def _tilt_stick(self, stick, x, y):
        assert stick in Stick
        assert 0 <= x <= 1 and 0 <= y <= 1
        self.pipe.write('SET {} {:.2f} {:.2f}\n'.format(stick.name, x, y))

    def tilt_control(self, stick, direction):
        assert stick in Stick
        assert direction in Direction
        self._tilt_stick(stick, direction.value[0], direction.value[1])
        time.sleep(.3)
        self._tilt_stick(stick, Direction.NEUTRAL.value[0], Direction.NEUTRAL.value[1])

    def hit_button(self, button):
        print "hitting %s" % button.value
        self._press_button(button)
        time.sleep(.25)
        self._release_button(button)
