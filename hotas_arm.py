# import asyncio
import threading
import sys

from joystick import Joystick

js      = None
arm     = None

class HOTAS_Arm(threading.Thread):

    def __init__(self, threadID, name, joystick, arm):
        threading.Thread.__init__(self)
        
        self.threadID       =   threadID
        self.name           =   name
        self.joystick       =   joystick
        self.arm            =   arm

    def run(self):
        print("In main")

        running = True
        while(running):
            pass
            # print("in main")
            # print(self.joystick.get_event_values())

def main():
    
    
    js = Joystick(1, "Thread - Joystick")
    arm = None

    hotas = HOTAS_Arm(1, "Thread - HOTAS", js, arm)
    
    js.start()
    hotas.start()
    
    
    js.join()
    hotas.join()

if __name__ == "__main__":
    main()