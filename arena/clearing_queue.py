import Queue


class ClearingQueue(Queue.Queue):
    def put(self, *args, **kwargs):
        print "put called"
        if self.full():
            print "full returned true"
            try:
                oldest_element = self.get(block=False)
                print "Throwing away old element: " + repr(oldest_element)
            except Queue.Empty:
                print "queue empty exception"
                pass

        Queue.Queue.put(self, *args, **kwargs)
