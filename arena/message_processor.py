import Queue
import time
import threading

from collections import deque
from controller import Button
from controller import Direction
from controller import Stick
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
                formatted = MessageProcessor.format_message(temp_message)
                self.message_buffer.append(formatted)
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
            pass
        finally:
            self.game_tick = threading.Timer(.3, self.get_controller_action)
            self.game_tick.start()
            return self.game_tick

    @staticmethod
    def format_message(message):
        text = message['message'].strip().lower()

        selected_control = None
        if text in ['press a', 'a']:
            selected_control = Button.A
        elif text in ['press b', 'b']:
            selected_control = Button.B
        elif text in ['press d up', 'd up']:
            selected_control = Button.D_UP
        elif text in ['press d down', 'd down']:
            selected_control = Button.D_DOWN
        elif text in ['press d right', 'd right']:
            selected_control = Button.D_RIGHT
        elif text in ['press d left', 'd left']:
            selected_control = Button.D_LEFT
        elif text in ['press start', 'start']:
            selected_control = Button.START
        elif text in ['press x', 'x']:
            selected_control = Button.X
        elif text in ['press y', 'y']:
            selected_control = Button.Y
        elif text in ['press z', 'z']:
            selected_control = Button.Z
        elif text == 'left':
            selected_control = Stick.MAIN
            message['direction'] = Direction.LEFT
        elif text == 'right':
            selected_control = Stick.MAIN
            message['direction'] = Direction.RIGHT
        elif text == 'up':
            selected_control = Stick.MAIN
            message['direction'] = Direction.UP
        elif text == 'down':
            selected_control = Stick.MAIN
            message['direction'] = Direction.DOWN
        elif text == 'up left':
            selected_control = Stick.MAIN
            message['direction'] = Direction.UP_LEFT
        elif text == 'up right':
            selected_control = Stick.MAIN
            message['direction'] = Direction.UP_RIGHT
        elif text == 'down left':
            selected_control = Stick.MAIN
            message['direction'] = Direction.DOWN_LEFT
        elif text == 'down right':
            selected_control = Stick.MAIN
            message['direction'] = Direction.DOWN_RIGHT

        if selected_control:
            message['control'] = selected_control

        return message
