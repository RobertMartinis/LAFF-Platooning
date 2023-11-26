import curses
from orchestrator.shared import *

class GUI:
    def __init__(self, std_scr):
        self.__std_scr = std_scr
        self.__out_win = None
        self.__client_win = None
        self.__status_win = None
        self.__setup()

    def __setup(self):
        curses.use_default_colors()
        if curses.has_colors():
            curses.start_color()

        sidebar_width = int((curses.COLS-1) / 3)
        socket_win_height = int((curses.LINES - 2) / 2)
        self.__out_win = curses.newwin(
            curses.LINES - 1, curses.COLS - sidebar_width - 1, 0, 0)
        self.__client_win = curses.newwin(
            socket_win_height, sidebar_width, 0, curses.COLS - sidebar_width)
        self.__socket_win = curses.newwin(
            socket_win_height, sidebar_width, socket_win_height, curses.COLS - sidebar_width)
        self.__cli_win = curses.newwin(
            1, curses.COLS - sidebar_width, curses.LINES - 1, 0)
        self.__status_win = curses.newwin(
            1, sidebar_width, curses.LINES - 1, curses.COLS - sidebar_width)

        curses.nocbreak()
        curses.curs_set(0)
        curses.echo()

        self.__out_win.scrollok(True)
        self.__client_win.scrollok(True)
        self.__socket_win.scrollok(True)
        self.__cli_win.keypad(True)
        self.__std_scr.clear()

    def help(self):
        self.output(AVAILABLE_COMMANDS_STR)
        self.__out_win.refresh()

    def welcome(self):
        self.output("Console", bold=True)
        self.output(f"LAFF orchestrator, listening on port {SOCKET_PORT}\n")
        self.help()

    def output(self, msg, win=None, bold=False):
        if win is None:
            win = self.__out_win
        msg_to_show = f"{msg}\n"
        if bold:
            win.addstr(msg_to_show, curses.A_BOLD)
        else:
            win.addstr(msg_to_show)
        win.refresh()

    def socket_output(self, msg):
        self.output(f"[ACK] {msg}", win=self.__socket_win)

    def update_nodes(self, nodes, master_node):
        self.__client_win.clear()
        if len(nodes) == 0:
            self.output("No connected nodes", win=self.__client_win, bold=True)
            return

        self.output("Connected nodes", win=self.__client_win, bold=True)
        for idx, node in enumerate(nodes):
            if node == master_node:
                self.output(f"{idx}) {node} (master)", win=self.__client_win)
                continue

            self.output(f"{idx}) {node}", win=self.__client_win)

        self.__client_win.refresh()

    def update_status(self, running, debug):
        self.__status_win.clear()
        running_state = "yes" if running else "no"
        debug_state = "yes" if debug else "no"
        self.__status_win.addstr(f"running: {running_state}")
        self.__status_win.addstr(" | ")
        self.__status_win.addstr(f"debug: {debug_state}")
        self.__status_win.refresh()

    def prompt(self):
        self.__cli_win.clear()
        self.__cli_win.addstr(0, 0, "cmd>", curses.A_BOLD)
        self.__cli_win.move(0, 5)
        msg = self.__cli_win.getstr().decode("utf-8")
        self.__out_win.addstr("execute> ", curses.A_BOLD)
        self.__out_win.addstr(f"{msg}\n")
        self.__out_win.refresh()
        return msg

    def clear_output(self):
        self.__out_win.clear()
        self.__out_win.refresh()
