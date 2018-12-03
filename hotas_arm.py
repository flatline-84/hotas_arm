# import asyncio
import threading
import sys
import time

from joystick import Joystick
from curses_screen import Screen

js      = None
arm     = None

class HOTAS_Arm(threading.Thread):

    def __init__(self, threadID, name, joystick, arm, js_lock, arm_lock, screen):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.threadID       =   threadID
        self.name           =   name
        self.joystick       =   joystick
        self.arm            =   arm
        self.js_lock        =   js_lock
        self.arm_lock       =   arm_lock
        self.screen         =   screen
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("In Main")

        while(not self.stopped()):
            data = self.joystick.get_event_values()
            self.screen.set_data(data)
            # time.sleep(1)
            # print("in main")
            # print(self.joystick.get_event_values())
        # print("Ending HOTAS")
        return

def main():
    
    # global exit_flag

    js_lock = threading.Lock()
    arm_lock = threading.Lock()

    js = Joystick(1, "Thread - Joystick", js_lock)
    arm = None

    screen = Screen()

    hotas = HOTAS_Arm(1, "Thread - HOTAS", js, arm, js_lock, arm_lock, screen)
    
    js.start()
    hotas.start()
    screen.start()

    screen.join()
    js.stop()
    print("Joystick asked to stop...")
    hotas.stop()
    print("Program asked to stop...")
    
    hotas.join()
    print("Main Ended")
    print("Please press a key on the joystick to end the program...")
    js.join()
    print("Program ended...")


if __name__ == "__main__":
    main()