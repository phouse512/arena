import Queue
import time
import threading

from collections import deque
from multiprocessing import Process


class MessageProcessor(Process):

    def __init__(self, controller_queue, message_queue):
        super(MessageProcessor, self).__init__()

        self.controller_queue = controller_queue
        self.message_queue = message_queue
        self.message_buffer = deque(maxlen=20)

    def run(self):
        print "running message processor"

        print "starting timer"
        self.game_tick = self.get_controller_action()

        while True:
            try:
                time.sleep(.1)
                temp_message = self.message_queue.get(block=False)
                # TODO add clean method to only put good messages
                print "mp message: %s" % str(temp_message)
                self.message_buffer.append(temp_message)
                print self.message_buffer
            except Queue.Empty:
                # print "empty but still processing"
                # print self.message_buffer
                pass

    def get_controller_action(self):
        print "calling get_controller_action"
        try:
            # print "buffer inside action: %s" % str(self.message_buffer)
            transfer_message = self.message_buffer.popleft()
            print "inside controller_action with message %s" % str(transfer_message)
            self.controller_queue.put(transfer_message, block=False)
        except IndexError as e:
            print "empty message_queue %s" % str(e)
            pass
        finally:
            self.game_tick = threading.Timer(1.0, self.get_controller_action)
            self.game_tick.start()
            return self.game_tick
