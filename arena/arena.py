import time

from controller import Button
from controller import Controller
from message_stream import TwitchStream


class Arena:

    def __init__(self):
        print "loading credentials"
        try:
            print "Starting arena now, press ^C to stop the arena"
            self.gametick = .3
            self.controller = Controller('/Users/PhilipHouse/Library/Application Support/Dolphin/Pipes/player1')
            self.chat_stream = TwitchStream()
            self.run()
        except KeyboardInterrupt:
            print "Stopped"

    def run(self):
        print "now running"
        while True:
            time.sleep(self.gametick)
            self.controller.hit_button(Button.A)

