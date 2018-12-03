import asyncio
import evdev
import threading

_BTN_TRIGGER    =   288
_BTN_SE         =   298
_BTN_ST         =   299
# bar thing on throttle
_BAR            =   6 #values from 0 (left) to 255 (right)
_THROTTLE       =   2 #values 255 (down) to 0 (full), 128 middle bump
_HNDL_PITCH     =   1 #values 0 (forward) to 1023 (backwards), 512 middle
_HNDL_ROLL      =   0 #values 0 (left) to 1023 (right), 512 middle
_HDNL_YAW       =   5 #values 0 (left) to 255 (right), 128 middle

# exit_flag       =   0
_DEBUG          =   False

class Joystick (threading.Thread):
    def __init__(self, threadID, name, lock):

        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.threadID       =   threadID
        self.name           =   name
        # self.counter        =   counter
        self.lock           =   lock

        self.dev            =   None

        # Set your controller name here
        self.device_name    =   "Thrustmaster T.Flight Hotas X"

        self.event_codes    =   {
            288         :   "_BTN_TRIGGER",#    :   288,
            298         :   "_BTN_SE",#         :   298,
            299         :   "_BTN_ST",#         :   299,
            # bar thing on throttle
            6           :   "_BAR",#            :   6, #values from 0 (left) to 255 (right)
            2           :   "_THROTTLE",#       :   2, #values 255 (down) to 0 (full), 128 middle bump
            1           :   "_HNDL_PITCH",#     :   1, #values 0 (forward) to 1023 (backwards), 512 middle
            0           :   "_HNDL_ROLL",#      :   0, #values 0 (left) to 1023 (right), 512 middle
            5           :   "_HDNL_YAW"#       :   5, #values 0 (left) to 255 (right), 128 middle
        }

        self.event_values   =   {
            "_BTN_TRIGGER"    :   0,
            "_BTN_SE"         :   0,
            "_BTN_ST"         :   0,
            # bar thing on throttle
            "_BAR"            :   0, #values from 0 (left) to 255 (right)
            "_THROTTLE"       :   0, #values 255 (down) to 0 (full), 128 middle bump
            "_HNDL_PITCH"     :   0, #values 0 (forward) to 1023 (backwards), 512 middle
            "_HNDL_ROLL"      :   0, #values 0 (left) to 1023 (right), 512 middle
            "_HDNL_YAW"       :   0, #values 0 (left) to 255 (right), 128 middle
        }

        self.set_device()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def set_device(self):
        if not self.find_device(self.get_current_devices()):
            print("Cannot find device!")
            exit(1)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.reader(self.dev))
    
    def run(self):
        print("Starting: " + self.name)
        self.th_reader()
        print("Exiting: " + self.name)

    async def reader(self):
        async for ev in self.dev.async_read_loop():
            # print(repr(ev))
            self.parse_event(ev)
    
    def th_reader(self):
        
        #Catching if no events fired and program ends **DOESN'T WORK**
        if self.stopped():
            return
        
        # This loop is annoying af. Let me pull the events one by one
        for ev in self.dev.read_loop():
            if _DEBUG:
                # print(repr(ev))
                pass
            # To fully quit, press button on controller
            if self.stopped():
                return
            self.parse_event(ev)

    def parse_event(self, ev):
        # print(ev.code)
        # if ev.code in self.event_codes.values():
        #     # self.event_values[ev.code]
        #     print (ev.value)

        # ev.code = 0 is roll but the type needs to be 3
        # otherwise a ghost event with ev.code = 0 and ev.type = 0 always occurs
        if (ev.code == 0 and ev.type != 3):
            return

        code = self.event_codes.get(ev.code)
        if code:
            # Lock self.event_values so that they can be updated
            # Will automatically acquire and release thanks to 'with'
            with self.lock:
                self.event_values[code] = ev.value
                if(_DEBUG):
                    print(code + ":" + str(ev.value))

    def get_event_values(self):
        with self.lock:
            return self.event_values

    def get_current_devices(self):
        return [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    def find_device(self, devices):
        for i in range(len(devices)):
            if devices[i].name == self.device_name:
                self.dev = devices[i]
                return True
        return False

if __name__ == "__main__":

    js_lock = threading.Lock()
    js = Joystick(1, "Thread - Joystick", js_lock)
    js.start()
    js.join()

    print("Exiting Joystick Main Thread")