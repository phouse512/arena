import time

from controller import Button
from controller import Controller
from message_stream import TwitchStream
from multiprocessing import Queue


class Arena:

    def __init__(self):
        print "loading credentials"
        try:
            print "Starting arena now, press ^C to stop the arena"
            self.gametick = 2
            # self.controller = Controller('/Users/PhilipHouse/Library/Application Support/Dolphin/Pipes/player1')

            self._thread_queue = Queue()

            self.chat_stream = TwitchStream(self._thread_queue)
            self.chat_stream.start()

            self.run()
        except KeyboardInterrupt:
            print "Stopped"
            self.chat_stream.join()

    def run(self):
        print "now running"
        while True:
            time.sleep(self.gametick)
            temp = self._thread_queue.get(block=False)
            print temp
            # self.controller.hit_button(Button.A)

