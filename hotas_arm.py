# import asyncio
import threading
import sys

import joystick

if __name__ == "__main__":
    js = joystick.Joystick()
    js.start()

    running = True
    while (running):
        print("am I here?")
        print(js.get_event_values())