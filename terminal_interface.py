import curses
import time

class Interface():

    def __init__(self, ):
        

    """
    Main loop for the user inteface
    """
    def curses(self, stdscr):
        curses.curs_set(0)

        h, w = stdscr.getmaxyx()

        text = "Hello, World!"

        x = w // 2 - len(text) // 2
        y = h // 2

        stdscr.addstr(y, x, text)
        stdscr.refresh()

        time.sleep(3)

    def run(self):
        curses.wrapper(self.curses)

if __name__ == "__main__":
    gui = Interface()
    gui.run()