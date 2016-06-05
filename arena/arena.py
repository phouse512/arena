import time
import threading
from Queue import Empty

from controller import Button
from controller import Controller
from message_processor import MessageProcessor
from message_stream import TwitchStream
from multiprocessing import Queue


class Arena:

    def __init__(self):
        print "loading credentials"
        try:
            print "Starting arena now, press ^C to stop the arena"
            self.gametick = 2
            self.controller = Controller('/Users/philhouse/Library/Application Support/Dolphin/Pipes/player1')

            self._message_queue = Queue()
            self._controller_queue = Queue()

            self.message_processor = MessageProcessor(
                self._controller_queue,
                self._message_queue
            )
            self.chat_stream = TwitchStream(
                self._message_queue
            )

            self.message_processor.start()
            self.chat_stream.start()

            # self.game_tick = self.fetch_action()
            self.run()

        except KeyboardInterrupt:
            print "Stopped"
            self.message_processor.join()
            self.chat_stream.join()
            # self.game_tick.cancel()

    def run(self):
        print "now running"
        while True:
            time.sleep(.01)
            # self.controller.hit_button(Button.A)
            try:
                control = self._controller_queue.get(block=False)
                if 'direction' in control:
                    self.controller.tilt_control(
                        control['control'],
                        control['direction']
                    )

                elif 'control' in control:
                    self.controller.hit_button(control['control'])
                print "receiving control: %s" % str(control)
            except Empty:
                pass

    def fetch_action(self):
        print "fetch action is called"

        self.message_processor.get_controller_action()
        self.game_tick = threading.Timer(1.0, self.fetch_action)
        self.game_tick.start()
        return self.game_tick
