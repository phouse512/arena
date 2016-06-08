import json
import requests
import threading
import time
from Queue import Empty

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

            # initialize contributions dictionary
            self.contributions = {}

            self.message_processor.start()
            self.chat_stream.start()

            # initialize requests call to update web and begin processing controls
            self.scoreboard_update = self.update_web()
            self.run()

        except KeyboardInterrupt:
            print "Stopped"
            self.message_processor.join()
            self.chat_stream.join()
            self.scoreboard_update.join()

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
                self.contributions[control['user']] = self.contributions.get(control['user'], 0) + 1
            except Empty:
                pass

    def update_web(self):
        """
        a method used for updating the web scoreboard with the current contributions
        :return: reference to timer object
        """
        headers = {'Content-Type': 'application/json'}
        print "inside update web"
        resp = requests.post('http://localhost:3000/update_contributors',
                             data=json.dumps(self.contributions),
                             timeout=1, headers=headers)
        print resp
        self.scoreboard_update = threading.Timer(2, self.update_web)
        self.scoreboard_update.start()
        return self.scoreboard_update
