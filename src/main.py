#!/usr/bin/env python3

########################################
# IMPORTS
########################################

import sys
import curses
import math

stdscreen = None

########################################
# EXIT CODE CONSTANTS
########################################

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

########################################
# MISCELLANEOUS CONSTANTS
########################################

PAIR_EMPTY = 1

data = []

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

########################################
# MAIN
########################################

def reset_data(screen, width, height):
    for j in range(height-1):
        for i in range(16):
            screen.addstr(j, i*3, "00", curses.color_pair(PAIR_EMPTY) | curses.A_BOLD)
            screen.addstr(j, (width-16)+i, ".", curses.color_pair(PAIR_EMPTY) | curses.A_BOLD)

    screen.move(0, 0)
    screen.refresh()

# C-style main function `int main(int argc, char** argv)`
def main(stdscreen):
    curses.use_default_colors()
    curses.init_pair(PAIR_EMPTY, curses.COLOR_BLACK, -1)
    height, width = stdscreen.getmaxyx()
    w, h = getTerminalSize()
    stdscreen.resize(height, w)
    height, width = stdscreen.getmaxyx()

    reset_data(stdscreen, width, height)

    while True:
        key = stdscreen.getch()
        y, x = stdscreen.getyx()

        if ((key >= ord('0') and key <= ord('9')) or (key >= ord('a') and key <= ord('f')) or (key >= ord('A') and key <= ord('F'))) and x < 16*3:
            stdscreen.addch(chr(key).upper())
            y, x = stdscreen.getyx()
            if x % 3 == 1:
                stdscreen.addch('0')
                stdscreen.move(y, x)
            y, x = stdscreen.getyx()
            if x % 3 == 2:
                stdscreen.addch(' ')
            y, x = stdscreen.getyx()
            if x >= 16*3:
                stdscreen.move(y+1, 0)
            stdscreen.refresh()
        elif key >= 258 and key <= 261:
            if key == 258:
                stdscreen.move(y+1, x)
            elif key == 259:
                stdscreen.move(y-1, x)
            elif key == 260:
                stdscreen.move(y, math.floor((x-3)/3)*3)
            elif key == 261:
                stdscreen.move(y, math.floor((x+3)/3)*3)

curses.wrapper(main)
