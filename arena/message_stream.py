import socket

from clearing_queue import ClearingQueue
from collections import deque
from multiprocessing import Process


class TwitchStream(Process):

    def __init__(self, queue):
        super(TwitchStream, self).__init__()
        print "starting message stream"
        self.oauth_token = 'oauth:yalia452t0539njju7go7bvrecwbkr'
        self.nick = 'wisotv'
        self.channel = 'wisotv'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queue = queue
        connect_status = self.chat_connect()
        if not connect_status:
            raise KeyboardInterrupt

    def __del__(self):
        print "closing message stream"

    def chat_connect(self):
        print "attempting to connect to twitch.tv"
        self.socket.settimeout(1.0)
        chat_host = "irc.chat.twitch.tv"
        chat_port = 6667

        try:
            self.socket.connect((chat_host, chat_port))
        except Exception:
            print "Failed to connect to twitch.tv"
            return False

        print "Connected to twitch! Passing credentials"
        self.socket.send("PASS %s\r\n" % self.oauth_token)
        self.socket.send("NICK %s\r\n" % self.nick)
        self.socket.send("JOIN #%s\r\n" % self.channel)

        return True

    def run(self):
        print "starting to process twitch messages in separate thread"
        counter = 0
        timeouts = 0
        while True:
            if timeouts == 10:
                print "received 10 timeouts.."
                timeouts = 0
            try:
                temp = self.socket.recv(1024)

                messages = filter(None, temp.split("\r\n"))

                for message in messages:
                    if message == 'PING :tmi.twitch.tv':
                        self.handle_ping()
                        continue
                    self.queue.put(message)

                print temp
                # counter += 1
                #
                # if counter == 5:
                #     print "at 5 messages"
                #     print list(self.queue)
                #     counter = 0
            except socket.timeout:
                timeouts += 1

    def handle_ping(self):
        print "received a ping..ponging!"
        self.socket.send("PONG :tmi.twitch.tv\r\n")
