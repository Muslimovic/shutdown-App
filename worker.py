import threading

class Worker(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self,target = target)
    def run(self):
        try:
            self._target()
        except:
            pass