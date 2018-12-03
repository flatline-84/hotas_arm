import curses
from curses import wrapper
import time
import threading

# exit_flag = 0

class Screen(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.data = None
        self.stdscr = None

        self.delay = 0
        self.title_string = "HOTAS Arm Controller"

        self.test_counter = 1

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def screen_main(self, stdscr):

        self.stdscr = stdscr

        stdscr.nodelay(1) #makes getch() non-blocking
        stdscr.refresh()        
        # Clear screen
        stdscr.clear()

        self.y, self.x = stdscr.getmaxyx()

        # returns tuple of (y,x) => (height, width)
        # stdscr.getmaxyx()
        self.start_time = time.clock() - self.delay #seconds
        self.end_time = time.clock()

        while True:
            #Update data
            self.draw_data()
            self.draw_title()
            #updates the window
            stdscr.refresh()

            self.end_time = time.clock()

            c = stdscr.getch()
            if c == ord('q'):
                self.stop()
                break
            elif c == ord('p'):
                self.test_counter += 1


        # stdscr.getkey()
    def draw_title(self):
        self.stdscr.addstr(0, int((self.x/2) - (len(self.title_string)/2)), self.title_string, curses.A_REVERSE)
        self.stdscr.addstr(1, 1, "Press 'q' to exit the program...")

    def draw_data(self):

        if (self.end_time - self.start_time > self.delay):
            self.stdscr.box()        
            if self.data is not None:
                # print("about to draw data")
                current_line = 3
                # print(self.data)

                for key, value in self.data.items():
                    self.stdscr.addstr(current_line, 2, key)
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(current_line, 20, str(value))

                    current_line += 1
            # self.stdscr.addstr(self.test_counter,2, "Yo my dude")

            # Clear from cursor to end of line
            # self.stdscr.clrtoeol()
            self.start_time = time.clock()

    def set_data(self, data):
        self.data = data
        # print("got data:")
        # print(self.data)

    def run(self):
        wrapper(self.screen_main)

if __name__ == "__main__":
    screen = Screen()
    screen.start()
    screen.join()