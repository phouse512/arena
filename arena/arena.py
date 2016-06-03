import time

from controller import Button
from controller import Controller
from message_stream import TwitchStream
from multiprocessing import Process


class Arena:

    def __init__(self):
        print "loading credentials"
        try:
            print "Starting arena now, press ^C to stop the arena"
            self.gametick = 2
            self.controller = Controller('/Users/PhilipHouse/Library/Application Support/Dolphin/Pipes/player1')
            self.chat_stream = TwitchStream()
            self.chat_stream.start()

            self.run()
        except KeyboardInterrupt:
            print "Stopped"
            self.chat_stream.join()

    def run(self):
        print "now running"
        while True:
            time.sleep(self.gametick)
            print list(self.chat_stream.queue.queue)
            self.controller.hit_button(Button.A)

