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

    def hit_button(self, button):
        print "hitting %s" % button.value
        self._press_button(button)
        time.sleep(.25)
        self._release_button(button)
