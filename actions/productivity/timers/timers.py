import time
import threading
import uuid


class TimerTool:

    name = "timer"

    def __init__(self):
        self.timers = {}


    def start_timer(self, seconds):
        timer_id = str(uuid.uuid4())

        timer = threading.Timer(seconds, lambda: print(f"Timer {timer_id} complete"))
        timer.start()

        self.timers[timer_id] = timer

        return timer_id
    

    def cancel_timer(self, timer_id):
        if timer_id in self.timers:
            self.timers[timer_id].cancel()

            return True
        
        return False