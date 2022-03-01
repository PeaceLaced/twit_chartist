

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/xmas.py'''
from __future__ import division
from asciimatics.effects import Cycle, Snow, Print
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys

# Tree definition
tree = r"""
       ${3,1}*
      / \
     /${1}o${2}  \
    /_   _\
     /   \${4}b
    /     \
   /   ${1}o${2}   \
  /__     __\
  ${1}d${2} / ${4}o${2}   \
   /       \
  / ${4}o     ${1}o${2}.\
 /___________\
      ${3}|||
      ${3}|||
""", r"""
       ${3}*
      / \
     /${1}o${2}  \
    /_   _\
     /   \${4}b
    /     \
   /   ${1}o${2}   \
  /__     __\
  ${1}d${2} / ${4}o${2}   \
   /       \
  / ${4}o     ${1}o${2} \
 /___________\
      ${3}|||
      ${3}|||
"""


def demo(screen):
    effects = [
        Print(screen, StaticRenderer(images=tree),
              x=screen.width - 15,
              y=screen.height - 15,
              colour=Screen.COLOUR_GREEN),
        Snow(screen),
        
        Cycle(
            screen,
            FigletText(""),
            #FigletText("HAPPY"),
            screen.height // 2 - 6,
            start_frame=300),
        Cycle(
            screen,
            FigletText(""),
            #FigletText("XMAS!"),
            screen.height // 2 + 1,
            start_frame=300),
        
    ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
    


'''https://github.com/peterbrittain/asciimatics/blob/master/samples/treeview.py
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, \
    Divider
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys
import os
try:
    import magic
except ImportError:
    pass


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Form")

        # Create the (very simple) form layout...
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        # Now populate it with the widgets we want to use.
        self._details = Text()
        self._details.disabled = True
        self._details.custom_colour = "field"
        self._list = FileBrowser(Widget.FILL_FRAME,
                                 os.path.abspath("."),
                                 name="mc_list",
                                 on_select=self.popup,
                                 on_change=self.details)
        layout.add_widget(Label("Local disk browser sample"))
        layout.add_widget(Divider())
        layout.add_widget(self._list)
        layout.add_widget(Divider())
        layout.add_widget(self._details)
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

        # Prepare the Frame for use.
        self.fix()

    def popup(self):
        # Just confirm whenever the user actually selects something.
        self._scene.add_effect(
            PopUpDialog(self._screen, "You selected: {}".format(self._list.value), ["OK"]))

    def details(self):
        # If python magic is installed, provide a little more detail of the current file.
        if self._list.value:
            if os.path.isdir(self._list.value):
                self._details.value = "Directory"
            elif os.path.isfile(self._list.value):
                try:
                    self._details.value = magic.from_file(self._list.value)
                except NameError:
                    self._details.value = "File (run 'pip install python-magic' for more details)"
        else:
            self._details.value = "--"

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        # Now pass on to lower levels for normal handling of the event.
        return super(DemoFrame, self).process_event(event)


def demo(screen, old_scene):
    screen.play([Scene([DemoFrame(screen)], -1)], stop_on_resize=True, start_scene=old_scene)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        
'''

# TOP sim, like TOP system resources app
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/top.py
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, MultiColumnListBox, Widget, Label, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.parsers import AsciimaticsParser
import sys
from collections import defaultdict
try:
    import psutil
except ImportError:
    print("This sample requires the psutil package.")
    print("Please run `pip install psutil` and try again.")
    sys.exit(0)


def readable_mem(mem):
    for suffix in ["", "K", "M", "G", "T"]:
        if mem < 10000:
            return "{}{}".format(int(mem), suffix)
        mem /= 1024
    return "{}P".format(int(mem))


def readable_pc(percent):
    if percent < 100:
        return str(round(percent * 10, 0) / 10)
    else:
        return str(int(percent))


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width,
                                        has_border=False,
                                        name="My Form")
        # Internal state required for doing periodic updates
        self._last_frame = 0
        self._sort = 5
        self._reverse = True

        # Create the basic form layout...
        layout = Layout([1], fill_frame=True)
        self._header = TextBox(1, as_string=True)
        self._header.disabled = True
        self._header.custom_colour = "label"
        self._list = MultiColumnListBox(
            Widget.FILL_FRAME,
            [">6", 10, ">4", ">7", ">7", ">5", ">5", "100%"],
            [],
            titles=["PID", "USER", "NI", "VIRT", "RSS", "CPU%", "MEM%", "CMD"],
            name="mc_list",
            parser=AsciimaticsParser())
        self.add_layout(layout)
        layout.add_widget(self._header)
        layout.add_widget(self._list)
        layout.add_widget(
            Label("Press `<`/`>` to change sort, `r` to toggle order, or `q` to quit."))
        self.fix()

        # Add my own colour palette
        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK))
        for key in ["selected_focus_field", "label"]:
            self.palette[key] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
        self.palette["title"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")
            elif event.key_code in [ord("r"), ord("R")]:
                self._reverse = not self._reverse
            elif event.key_code == ord("<"):
                self._sort = max(0, self._sort - 1)
            elif event.key_code == ord(">"):
                self._sort = min(7, self._sort + 1)

            # Force a refresh for improved responsiveness
            self._last_frame = 0

        # Now pass on to lower levels for normal handling of the event.
        return super(DemoFrame, self).process_event(event)

    def _update(self, frame_no):
        # Refresh the list view if needed
        if frame_no - self._last_frame >= self.frame_update_count or self._last_frame == 0:
            self._last_frame = frame_no

            # Create the data to go in the multi-column list...
            last_selection = self._list.value
            last_start = self._list.start_line
            list_data = []
            for process in psutil.process_iter():
                try:
                    memory = process.memory_info()
                    data = [
                        process.pid,
                        process.username(),
                        int(process.nice()),
                        memory.vms,
                        memory.rss,
                        process.cpu_percent(),
                        process.memory_percent(),
                        (" ".join(process.cmdline()) if process.cmdline() else
                         "[{}]".format(process.name()))
                    ]
                    list_data.append(data)
                except psutil.AccessDenied:
                    # Some platforms don't allow querying of all processes...
                    pass

            # Apply current sort and reformat for humans
            list_data = sorted(list_data,
                               key=lambda f: f[self._sort],
                               reverse=self._reverse)
            new_data = [
                ([
                    str(x[0]),
                    x[1],
                    str(x[2]),
                    readable_mem(x[3]),
                    readable_mem(x[4]),
                    readable_pc(x[5]),
                    readable_pc(x[6]),
                    x[7]
                ], x[0]) for x in list_data
            ]

            # Add colours...
            coloured_data = []
            for cols, val in new_data:
                cpu = float(cols[5])
                if cpu < 40:
                    colour = ""
                elif cpu < 60:
                    colour = "${3}"
                elif cpu < 80:
                    colour = "${1}"
                else:
                    colour = "${1,1}"
                coloured_data.append(([colour + x for x in cols], val))

            # Update the list and try to reset the last selection.
            self._list.options = coloured_data
            self._list.value = last_selection
            self._list.start_line = last_start
            self._header.value = (
                "CPU usage: {}%   Memory available: {}M".format(
                    str(round(psutil.cpu_percent() * 10, 0) / 10),
                    str(int(psutil.virtual_memory().available / 1024 / 1024))))

        # Now redraw as normal
        super(DemoFrame, self)._update(frame_no)

    @property
    def frame_update_count(self):
        # Refresh once every 2 seconds by default.
        return 40


def demo(screen):
    screen.play([Scene([DemoFrame(screen)], -1)], stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True)
            sys.exit(0)
        except ResizeScreenError:
            pass
    
'''

# PSEUDO TTY bash shell
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/terminal.py
from asciimatics.widgets import Frame, Layout, Widget
from asciimatics.effects import Background
from asciimatics.scene import Scene
from asciimatics.screen import Screen, Canvas
from asciimatics.exceptions import ResizeScreenError
from asciimatics.parsers import AnsiTerminalParser, Parser
from asciimatics.event import KeyboardEvent
import sys
import subprocess
import threading
try:
    import select
    import pty
    import os
    import fcntl
    import curses
    import struct
    import termios
except Exception:
    print("This demo only runs on Unix systems.")
    sys.exit(0)


class Terminal(Widget):
    """
    Widget to handle ansi terminals running a bash shell.
    The widget will start a bash shell in the background and use a pseudo TTY to control it.  It then
    starts a thread to transfer any data between the two processes (the one running this widget and
    the bash shell).
    """
    def __init__(self, name, height):
        super(Terminal, self).__init__(name)
        self._required_height = height
        self._parser = AnsiTerminalParser()
        self._canvas = None
        self._current_colours = None
        self._cursor_x, self._cursor_y = 0, 0
        self._show_cursor = True

        # Supported key mappings
        self._map = {}
        for k, v in [
            (Screen.KEY_LEFT, "kcub1"),
            (Screen.KEY_RIGHT, "kcuf1"),
            (Screen.KEY_UP, "kcuu1"),
            (Screen.KEY_DOWN, "kcud1"),
            (Screen.KEY_PAGE_UP, "kpp"),
            (Screen.KEY_PAGE_DOWN, "knp"),
            (Screen.KEY_HOME, "khome"),
            (Screen.KEY_END, "kend"),
            (Screen.KEY_DELETE, "kdch1"),
            (Screen.KEY_BACK, "kbs"),
        ]:
            self._map[k] = curses.tigetstr(v)
        self._map[Screen.KEY_TAB] = "\t".encode()

        # Open a pseudo TTY to control the interactive session.  Make it non-blocking.
        self._master, self._slave = pty.openpty()
        fl = fcntl.fcntl(self._master, fcntl.F_GETFL)
        fcntl.fcntl(self._master, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # Start the shell and thread to pull data from it.
        self._shell = subprocess.Popen(
            ["bash", "-i"], preexec_fn=os.setsid, stdin=self._slave, stdout=self._slave, stderr=self._slave)
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._background)
        self._thread.daemon = True
        self._thread.start()

    def set_layout(self, x, y, offset, w, h):
        """
        Resize the widget (and underlying TTY) to the required size.
        """
        super(Terminal, self).set_layout(x, y, offset, w, h)
        self._canvas = Canvas(self._frame.canvas, h, w, x=x, y=y)
        winsize = struct.pack("HHHH", h, w, 0, 0)
        fcntl.ioctl(self._slave, termios.TIOCSWINSZ, winsize)

    def update(self, frame_no):
        """
        Draw the current terminal content to screen.
        """
        # Don't allow background thread to update values mid screen refresh.
        with self._lock:
            # Push current terminal output to screen.
            self._canvas.refresh()

            # Draw cursor if needed.
            if frame_no % 10 < 5 and self._show_cursor:
                origin = self._canvas.origin
                x = self._cursor_x + origin[0]
                y = self._cursor_y + origin[1] - self._canvas.start_line
                details = self._canvas.get_from(self._cursor_x, self._cursor_y)
                if details:
                    char, colour, attr, bg = details
                    attr |= Screen.A_REVERSE
                    self._frame.canvas.print_at(chr(char), x, y, colour, attr, bg)

    def process_event(self, event):
        """
        Pass any recognised input on to the TTY.
        """
        if isinstance(event, KeyboardEvent):
            if event.key_code > 0:
                os.write(self._master, chr(event.key_code).encode())
                return
            elif event.key_code in self._map:
                os.write(self._master, self._map[event.key_code])
                return
        return event

    def _add_stream(self, value):
        """
        Process any output from the TTY.
        """
        lines = value.split("\n")
        for i, line in enumerate(lines):
            self._parser.reset(line, self._current_colours)
            for offset, command, params in self._parser.parse():
                if command == Parser.DISPLAY_TEXT:
                    # Just display the text...  allowing for line wrapping.
                    if self._cursor_x + len(params) > self._w:
                        part_1 = params[:self._w - self._cursor_x]
                        part_2 = params[self._w - self._cursor_x:]
                        self._print_at(part_1, self._cursor_x, self._cursor_y)
                        self._print_at(part_2, 0, self._cursor_y + 1)
                        self._cursor_x = len(part_2)
                        self._cursor_y += 1
                        if self._cursor_y - self._canvas.start_line >= self._h:
                            self._canvas.scroll()
                    else:
                        self._print_at(params, self._cursor_x, self._cursor_y)
                        self._cursor_x += len(params)
                elif command == Parser.CHANGE_COLOURS:
                    # Change current text colours.
                    self._current_colours = params
                elif command == Parser.NEXT_TAB:
                    # Move to next tab stop - hard-coded to default of 8 characters.
                    self._cursor_x = (self._cursor_x // 8) * 8 + 8
                elif command == Parser.MOVE_RELATIVE:
                    # Move cursor relative to current position.
                    self._cursor_x += params[0]
                    self._cursor_y += params[1]
                    if self._cursor_y < self._canvas.start_line:
                        self._canvas.scroll(self._cursor_y - self._canvas.start_line)
                elif command == Parser.MOVE_ABSOLUTE:
                    # Move cursor relative to specified absolute position.
                    if params[0] is not None:
                        self._cursor_x = params[0]
                    if params[1] is not None:
                        self._cursor_y = params[1] + self._canvas.start_line
                elif command == Parser.DELETE_LINE:
                    # Delete some/all of the current line.
                    if params == 0:
                        self._print_at(" " * (self._w - self._cursor_x), self._cursor_x, self._cursor_y)
                    elif params == 1:
                        self._print_at(" " * self._cursor_x, 0, self._cursor_y)
                    elif params == 2:
                        self._print_at(" " * self._w, 0, self._cursor_y)
                elif command == Parser.DELETE_CHARS:
                    # Delete n characters under the cursor.
                    for x in range(self._cursor_x, self._w):
                        if x + params < self._w:
                            cell = self._canvas.get_from(x + params, self._cursor_y)
                        else:
                            cell = (ord(" "),
                                    self._current_colours[0],
                                    self._current_colours[1],
                                    self._current_colours[2])
                        self._canvas.print_at(
                            chr(cell[0]), x, self._cursor_y, colour=cell[1], attr=cell[2], bg=cell[3])
                elif command == Parser.SHOW_CURSOR:
                    # Show/hide the cursor.
                    self._show_cursor = params
                elif command == Parser.CLEAR_SCREEN:
                    # Clear the screen.
                    self._canvas.clear_buffer(
                        self._current_colours[0], self._current_colours[1], self._current_colours[2])
            # Move to next line, scrolling buffer as needed.
            if i != len(lines) - 1:
                self._cursor_x = 0
                self._cursor_y += 1
                if self._cursor_y - self._canvas.start_line >= self._h:
                    self._canvas.scroll()

    def _print_at(self, text, x, y):
        """
        Helper function to simplify use of the canvas.
        """
        self._canvas.print_at(
            text,
            x, y,
            colour=self._current_colours[0], attr=self._current_colours[1], bg=self._current_colours[2])

    def _background(self):
        """
        Backround thread running the IO between the widget and the TTY session.
        """
        while True:
            ready, _, _ = select.select([self._master], [], [])
            for stream in ready:
                value = ""
                while True:
                    try:
                        data = os.read(stream, 102400)
                        data = data.decode("utf8", "replace")
                        value += data
                    # Python 2 and 3 raise different exceptions when they would block
                    except Exception:
                        with self._lock:
                            self._add_stream(value)
                            self._frame.screen.force_update()
                        break

    def reset(self):
        """
        Reset the widget to a blank screen.
        """
        self._canvas = Canvas(self._frame.canvas, self._h, self._w, x=self._x, y=self._y)
        self._cursor_x, self._cursor_y = 0, 0
        self._current_colours = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)

    def required_height(self, offset, width):
        """
        Required height for the terminal.
        """
        return self._required_height

    @property
    def frame_update_count(self):
        """
        Frame update rate required.
        """
        # Force refresh for cursor.
        return 5

    @property
    def value(self):
        """
        Terminal value - not needed for demo.
        """
        return

    @value.setter
    def value(self, new_value):
        return


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen, screen.height, screen.width)

        # Create the widgets for the demo.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Terminal("term", Widget.FILL_FRAME))
        self.fix()
        self.set_theme("monochrome")


def demo(screen, scene):
    screen.play([
        Scene([
            Background(screen),
            DemoFrame(screen)
        ], -1)
    ], stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        
'''        

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/simple.py
from __future__ import division
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen


def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 8),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3),
        Stars(screen, (screen.width + screen.height) // 2)
    ]
    screen.play([Scene(effects, 500)])

def run():
    Screen.wrapper(demo)
'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/rendering.py
from asciimatics.renderers import BarChart
from asciimatics.screen import Screen
import sys
import math
import time
from random import randint


def fn():
    return randint(0, 40)


def wv(x):
    return lambda: 1 + math.sin(math.pi * (2*time.time()+x) / 5)


def demo():
    chart = BarChart(10, 40, [fn, fn],
                     char="=",
                     gradient=[(20, Screen.COLOUR_GREEN),
                               (30, Screen.COLOUR_YELLOW),
                               (40, Screen.COLOUR_RED)])
    print(chart)
    chart = BarChart(13, 60,
                     [wv(1), wv(2), wv(3), wv(4), wv(5), wv(7), wv(8), wv(9)],
                     colour=Screen.COLOUR_GREEN,
                     axes=BarChart.BOTH,
                     scale=2.0)
    print(chart)
    chart = BarChart(7, 60, [lambda: time.time() * 10 % 101],
                     gradient=[(10, 234), (20, 236), (30, 238), (40, 240),
                               (50, 242), (60, 244), (70, 246), (80, 248),
                               (90, 250), (100, 252)],
                     char=">",
                     scale=100.0,
                     labels=True,
                     axes=BarChart.X_AXIS)
    print(chart)
    chart = BarChart(10, 60,
                     [wv(1), wv(2), wv(3), wv(4), wv(5), wv(7), wv(8), wv(9)],
                     colour=[c for c in range(1, 8)],
                     scale=2.0,
                     axes=BarChart.X_AXIS,
                     intervals=0.5,
                     labels=True,
                     border=False)
    print(chart)

def run():
    demo()
    sys.exit(0)

'''

        
# same as forms
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/quick_model.py
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys


class ContactModel(object):
    def __init__(self):
        # Current contact when editing.
        self.current_id = None

        # List of dicts, where each dict contains a single contact, containing
        # name, address, phone, email and notes fields.
        self.contacts = []


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Contact List")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            [(x["name"], i) for i,x in enumerate(self._model.contacts)],
            name="contacts",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = [(x["name"], i) for i,x in enumerate(self._model.contacts)]
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        del self._model.contacts[self.data["contacts"]]
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        if self._model.current_id is None:
            self.data = {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            self.data = self._model.contacts[self._model.current_id]

    def _ok(self):
        self.save()
        if self._model.current_id is None:
            self._model.contacts.append(self.data)
        else:
            self._model.contacts[self._model.current_id] = self.data
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


def demo(screen, scene):
    scenes = [
        Scene([ListView(screen, contacts)], -1, name="Main"),
        Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = ContactModel()
last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        
'''

        
# NOT WORKING, investigate renderers, feeling this is from old version
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/player.py
import sys
import logging
from asciimatics.effects import Print
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.ren
from asciimatics.renderers import AnsiArtPlayer, AsciinemaPlayer, SpeechBubble
from asciimatics.exceptions import ResizeScreenError

logging.basicConfig(filename="debug.log", level=logging.DEBUG)


def demo(screen, scene):
    with AsciinemaPlayer("test.rec", max_delay=0.1) as player, \
            AnsiArtPlayer("fruit.ans") as player2:
        screen.play(
            [
                Scene(
                    [
                        Print(screen, player, 0, speed=1, transparent=False),
                        Print(screen,
                              SpeechBubble("Press space to see ansi art"),
                              y=screen.height - 3, speed=0, transparent=False)
                    ], -1),
                Scene(
                    [
                        Print(screen, player2, 0, speed=1, transparent=False),
                        Print(screen,
                              SpeechBubble("Press space to see asciinema"),
                              y=screen.height - 3, speed=0, transparent=False)
                    ], -1)
            ],
            stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
def run(last_scene =None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        
'''
# NOT WORKING
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/particles.py
from random import randint
from asciimatics.effects import Print
from asciimatics.particles import Explosion, StarFirework, DropScreen, Rain, ShootScreen
from asciimatics.renderers import SpeechBubble, FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    screen.set_title("ASCIIMATICS demo")

    scenes = []

    # First scene: title page
    effects = [
        Print(screen,
              Rainbow(screen, FigletText("ASCIIMATICS", font="big")),
              y=screen.height // 4 - 5),
        Print(screen,
              FigletText("Particle System"),
              screen.height // 2 - 3),
        Print(screen,
              FigletText("Effects Demo"),
              screen.height * 3 // 4 - 3),
        Print(screen,
              SpeechBubble("Press SPACE to continue..."),
              screen.height - 3,
              transparent=False,
              start_frame=70)
    ]
    scenes.append(Scene(effects, -1))

    # Next scene: just dissolve the title.
    effects = []
    for i in range(8):
        effects.append(ShootScreen(
            screen,
            randint(screen.width // 3, screen.width * 2 // 3),
            randint(screen.height // 4, screen.height * 3 // 4),
            100,
            diameter=randint(8, 12),
            start_frame=i * 10))
    effects.append(ShootScreen(
            screen, screen.width // 2, screen.height // 2, 100, start_frame=90))
    scenes.append(Scene(effects, 120, clear=False))

    # Next scene: sub-heading.
    effects = [
        DropScreen(screen, 100),
        Print(screen,
              Rainbow(screen, FigletText("Explosions", font="doom")),
              y=screen.height // 2 - 5,
              stop_frame=30),
        DropScreen(screen, 100, start_frame=30)
    ]
    scenes.append(Scene(effects, 80))

    # Next scene: explosions
    effects = []
    for _ in range(20):
        effects.append(
            Explosion(screen,
                      randint(3, screen.width - 4),
                      randint(1, screen.height - 2),
                      randint(20, 30),
                      start_frame=randint(0, 250)))
    effects.append(Print(screen,
                         SpeechBubble("Press SPACE to continue..."),
                         screen.height - 6,
                         speed=1,
                         transparent=False,
                         start_frame=100))
    scenes.append(Scene(effects, -1))

    # Next scene: sub-heading.
    effects = [
        Print(screen,
              Rainbow(screen, FigletText("Rain", font="doom")),
              y=screen.height // 2 - 5,
              stop_frame=30),
        DropScreen(screen, 100, start_frame=30)
    ]
    scenes.append(Scene(effects, 80))

    # Next scene: rain storm.
    effects = [
        Rain(screen, 200),
        Print(screen,
              SpeechBubble("Press SPACE to continue..."),
              screen.height - 6,
              speed=1,
              transparent=False,
              start_frame=100)
    ]
    scenes.append(Scene(effects, -1))

    # Next scene: sub-heading.
    effects = [
        Print(screen,
              Rainbow(screen, FigletText("Fireworks", font="doom")),
              y=screen.height // 2 - 5,
              stop_frame=30),
        DropScreen(screen, 100, start_frame=30)
    ]
    scenes.append(Scene(effects, 80))

    # Next scene: fireworks
    effects = []
    for _ in range(20):
        effects.append(
            StarFirework(screen,
                         randint(3, screen.width - 4),
                         randint(1, screen.height - 2),
                         randint(20, 30),
                         start_frame=randint(0, 250)))
    effects.append(Print(screen,
                         SpeechBubble("Press SPACE to continue..."),
                         screen.height - 6,
                         speed=1,
                         transparent=False,
                         start_frame=100))
    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/pacman.py
from copy import deepcopy
import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Sprite, BannerText

namco = """
88888888b.  8888888b. 8888888888b. .d88888888 .d888888b.
88      88         88 88   88   88 88         88      88
88      88 .d88888888 88   88   88 88         88      88
88      88 88      88 88   88   88 88         88      88
88      88 `888888888 88   88   88 `888888888 `8888888P'
"""

dot = """${7,2,7}####
${7,2,7}####
"""

pac_man = """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
{0}##########################
{0}##########################
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
{0}##########################
              {0}############
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
      {0}####################
              {0}############
      {0}####################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
      {0}####################
          {0}################
              {0}############
          {0}################
      {0}####################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
    {0}##########${{4,2,0}}  ${{7,2,7}}  {0}######
        {0}##################
            {0}##############
              {0}############
            {0}##############
        {0}##################
    {0}####################
  {0}######################
    {0}##################
        {0}##########
"""

pac_man_right = """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}##########################
{0}##########################
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}##########################
{0}############
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}####################
{0}############
{0}####################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}####################
{0}################
{0}############
{0}################
{0}#####################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}##########
{0}##################
{0}##############
{0}############
{0}##############
{0}##################
  {0}####################
  {0}######################
    {0}##################
        {0}##########
"""

ghost = """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}##########################
{0}####${{7,2,0}}  {0}########${{7,2,0}}  {0}########
{0}##${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}######${{7,2,0}}  {0}########${{7,2,0}}  {0}########
{0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}########
  {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
  {0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}######
    {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}##${{7,2,0}}  {0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}####
      {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}##
"""

scared_ghost = """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}####${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}##
${4,2,4}##${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}##${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}####
      ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}##
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}######
    ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########
  ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}######${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########
${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
"""

eyes = """
    ${4,2,4}####${4,2,0}        ${4,2,4}####
  ${7,2,7}..${4,2,4}####${7,2,7}..${7,2,0}    ${7,2,7}..${4,2,4}####${7,2,7}..
  ${7,2,7}........${7,2,0}    ${7,2,7}........
  ${7,2,7}........${7,2,0}    ${7,2,7}........
    ${7,2,7}....${7,2,0}        ${7,2,7}....
"""

# Globals used for pacman animation
direction = 1
value = 0


def cycle():
    global value, direction
    value += direction
    if value <= 0 or value >= 4:
        direction = -direction
    return value


class PacMan(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        images = []
        images_right = []
        colour = Screen.COLOUR_YELLOW if screen.colours <= 16 else 11
        for image in pac_man:
            images.append(image.format("${%d,2,%d}" % (colour, colour)))
        for image in pac_man_right:
            images_right.append(image.format("${%d,2,%d}" % (colour, colour)))
        super(PacMan, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=images, animation=cycle),
                "left": StaticRenderer(images=images, animation=cycle),
                "right": StaticRenderer(images=images_right, animation=cycle),
            },
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)

    def _update(self, frame_no):
        super(PacMan, self)._update(frame_no)
        for effect in self._scene.effects:
            if isinstance(effect, ScaredGhost) and self.overlaps(effect):
                effect.eaten()


class Ghost(Sprite):
    def __init__(self, screen, path, colour=1, start_frame=0, stop_frame=0):
        images = []
        for image in ghost:
            images.append(image.format("${%d,2,%d}" % (colour, colour)))
        super(Ghost, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=images),
            },
            colour=colour,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)


class ScaredGhost(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        super(ScaredGhost, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=scared_ghost),
            },
            colour=Screen.COLOUR_BLUE,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)
        self._eaten = False

    def eaten(self):
        # Already eaten - just ignore
        if self._eaten:
            return

        # Allow one more iteration for this Sprite to clear itself up.
        self._eaten = True
        self._delete_count = 2

        # Spawn the eyes to run away
        path = Path()
        path.jump_to(self._old_x + 12, self._old_y + 4)
        path.move_straight_to(
            self._old_x + 12, -8, (self._old_y + 12) // 2)
        path.wait(10000)
        self._scene.add_effect(Eyes(self._screen, path))


class Eyes(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        super(Eyes, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=[eyes]),
            },
            colour=Screen.COLOUR_BLUE,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)


class EatingScene(Scene):
    def __init__(self, screen):
        super(EatingScene, self).__init__([], 240 + screen.width)
        self._screen = screen
        self._reset_count = 0

    def reset(self, old_scene=None, screen=None):
        super(EatingScene, self).reset(old_scene, screen)

        # Recreate all the elements.
        centre = (self._screen.width // 2, self._screen.height // 2)
        path = Path()
        path.jump_to(-16, centre[1])
        path.move_straight_to(
            self._screen.width + 16, centre[1], (self._screen.width + 16) // 3)
        path.wait(100)
        path2 = Path()
        path2.jump_to(-16, centre[1])
        path2.move_straight_to(
            self._screen.width + 16, centre[1], self._screen.width + 16)
        path2.wait(100)

        # Take a copy of the list before using it to remove all effects.
        for effect in self.effects[:]:
            self.remove_effect(effect)

        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2)))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=60))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=120))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=180))
        self.add_effect(PacMan(self._screen, path, start_frame=240))


def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)

    # Title
    effects = [
        BannerText(screen,
                   ColourImageFile(screen, "twit/free/img/pacman.png", 16, 0, True),
                   (screen.height - 16) // 2,
                   Screen.COLOUR_WHITE),
        Print(screen,
              StaticRenderer(images=["A tribute to the classic 80's "
                                     "video game by Namco."]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects, 0))

    # Scene 1 - run away, eating dots
    path = Path()
    path.jump_to(screen.width + 16, centre[1])
    path.move_straight_to(-16, centre[1], (screen.width + 16) // 3)
    path.wait(100)

    if screen.colours <= 16:
        inky = 6
        pinky = 5
        blinky = 1
        clyde = 2
    else:
        inky = 14
        pinky = 201
        blinky = 9
        clyde = 208

    effects = [
        PacMan(screen, path),
        Ghost(screen, deepcopy(path), inky, start_frame=40),
        Ghost(screen, deepcopy(path), pinky, start_frame=60),
        Ghost(screen, deepcopy(path), blinky, start_frame=80),
        Ghost(screen, deepcopy(path), clyde, start_frame=100),
    ]

    for x in range(5, screen.width, 16):
        effects.insert(0,
                       Print(screen,
                             StaticRenderer(images=[dot]),
                             screen.height // 2,
                             x=x,
                             speed=1,
                             stop_frame=4))

    scenes.append(Scene(effects, 100 + screen.width))

    # Scene 2 - Chase ghosts after a power pill
    scenes.append(EatingScene(screen))

    # Scene 3 - Thanks...
    effects = [
        Print(screen, FigletText("Thank you,"), screen.height // 3 - 3,
              colour=Screen.COLOUR_RED),
        Print(screen,
              StaticRenderer(images=[namco]),
              screen.height * 2 // 3 - 2,
              colour=Screen.COLOUR_RED),
        Print(screen,
              StaticRenderer(images=["< Press X to exit. >"]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects, 0))

    screen.play(scenes, stop_on_resize=True, repeat=False)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
        
'''
        
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/noise.py
from asciimatics.effects import RandomNoise
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    effects = [
        RandomNoise(screen,
                    signal=Rainbow(screen,
                                   FigletText("ASCIIMATICS")))
    ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''    
    
# NOT TESTED, requires API key for mapbox.com
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/maps.py
from __future__ import division
from __future__ import print_function
import traceback
from math import pi, exp, atan, log, tan, sqrt
import sys
import os
import json
import threading
from ast import literal_eval
from collections import OrderedDict
from asciimatics.event import KeyboardEvent
from asciimatics.renderers import ColourImageFile
from asciimatics.effects import Effect
from asciimatics.widgets import Button, Text, Layout, Frame, Divider, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication, InvalidFields
try:
    import mapbox_vector_tile
    import requests
    from google.protobuf.message import DecodeError
except ImportError:
    print("Run `pip install mapbox-vector-tile protobuf requests` to fix your dependencies.")
    print("See https://github.com/Toblerity/Shapely#installing-shapely-16b2 for Shapely install.")
    sys.exit(0)

# Global constants for the applications
# Replace `_KEY` with the free one that you get from signing up with www.mapbox.com
_KEY = ""
_VECTOR_URL = \
    "http://a.tiles.mapbox.com/v4/mapbox.mapbox-streets-v7/{}/{}/{}.mvt?access_token={}"
_IMAGE_URL = \
    "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{}/{}/{}?access_token={}"
_START_SIZE = 64
_ZOOM_IN_SIZE = _START_SIZE * 2
_ZOOM_OUT_SIZE = _START_SIZE // 2
_ZOOM_ANIMATION_STEPS = 6
_ZOOM_STEP = exp(log(2) / _ZOOM_ANIMATION_STEPS)
_CACHE_SIZE = 180
_HELP = """
You can moved around using the cursor keys.  To jump to any location in the world, press Enter and \
then fill in the longitude and latitude of the location and press 'OK'.
To zoom in and out use '+'/'-'.  To zoom all the way in/out, press '9'/'0'.
To swap between satellite and vector views, press 'T'.  To quit, press 'Q'.
"""


class EnterLocation(Frame):
    """Form to enter a new desired location to display on the map."""
    def __init__(self, screen, longitude, latitude, on_ok):
        super(EnterLocation, self).__init__(
            screen, 7, 40, data={"long": str(longitude), "lat": str(latitude)}, name="loc",
            title="Enter New Location", is_modal=True)
        self._on_ok = on_ok
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False), 1)
        layout.add_widget(Text(label="Longitude:", name="long", validator=r"^[-]?\d+?\.\d+?$"), 1)
        layout.add_widget(Text(label="Latitude:", name="lat", validator=r"^[-]?\d+?\.\d+?$"), 1)
        layout.add_widget(Divider(draw_line=False), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 1)
        layout2.add_widget(Button("Cancel", self._cancel), 2)
        self.fix()

    def _ok(self):
        try:
            self.save(validate=True)
        except InvalidFields:
            return
        self._on_ok(self)
        self._scene.remove_effect(self)

    def _cancel(self):
        self._scene.remove_effect(self)


class Map(Effect):
    """Effect to display a satellite image or vector map of the world."""

    # Colour palettes
    _256_PALETTE = {
        "landuse": 193,
        "water": 153,
        "waterway": 153,
        "marine_label": 12,
        "admin": 7,
        "country_label": 9,
        "state_label": 1,
        "place_label": 0,
        "building": 252,
        "road": 15,
        "poi_label": 8
    }
    _16_PALETTE = {
        "landuse": Screen.COLOUR_GREEN,
        "water": Screen.COLOUR_BLUE,
        "waterway": Screen.COLOUR_BLUE,
        "marine_label": Screen.COLOUR_BLUE,
        "admin": Screen.COLOUR_WHITE,
        "country_label": Screen.COLOUR_RED,
        "state_label": Screen.COLOUR_RED,
        "place_label": Screen.COLOUR_YELLOW,
        "building": Screen.COLOUR_WHITE,
        "road": Screen.COLOUR_WHITE,
        "poi_label": Screen.COLOUR_RED
    }

    def __init__(self, screen):
        super(Map, self).__init__(screen)
        # Current state of the map
        self._screen = screen
        self._zoom = 0
        self._latitude = 51.4778
        self._longitude = -0.0015
        self._tiles = OrderedDict()
        self._size = _START_SIZE
        self._satellite = False

        # Desired viewing location and animation flags
        self._desired_zoom = self._zoom
        self._desired_latitude = self._latitude
        self._desired_longitude = self._longitude
        self._next_update = 100000

        # State for the background thread which reads in the tiles
        self._running = True
        self._updated = threading.Event()
        self._updated.set()
        self._oops = None
        self._thread = threading.Thread(target=self._get_tiles)
        self._thread.daemon = True
        self._thread.start()
        
        # a separate directory to store cached files.
        if not os.path.isdir('mapscache'):
            os.mkdir('mapscache')

    def _scale_coords(self, x, y, extent, xo, yo):
        """Convert from tile coordinates to "pixels" - i.e. text characters."""
        return xo + (x * self._size * 2 / extent), yo + ((extent - y) * self._size / extent)

    def _convert_longitude(self, longitude):
        """Convert from longitude to the x position in overall map."""
        return int((180 + longitude) * (2 ** self._zoom) * self._size / 360)

    def _convert_latitude(self, latitude):
        """Convert from latitude to the y position in overall map."""
        return int((180 - (180 / pi * log(tan(
            pi / 4 + latitude * pi / 360)))) * (2 ** self._zoom) * self._size / 360)

    def _inc_lat(self, latitude, delta):
        """Shift the latitude by the required number of pixels (i.e. text lines)."""
        y = self._convert_latitude(latitude)
        y += delta
        return 360 / pi * atan(
            exp((180 - y * 360 / (2 ** self._zoom) / self._size) * pi / 180)) - 90

    def _get_satellite_tile(self, x_tile, y_tile, z_tile):
        """Load up a single satellite image tile."""
        cache_file = "mapscache/{}.{}.{}.jpg".format(z_tile, x_tile, y_tile)
        if cache_file not in self._tiles:
            if not os.path.isfile(cache_file):
                url = _IMAGE_URL.format(z_tile, x_tile, y_tile, _KEY)
                data = requests.get(url).content
                with open(cache_file, 'wb') as f:
                    f.write(data)
            self._tiles[cache_file] = [
                x_tile, y_tile, z_tile,
                ColourImageFile(self._screen, cache_file, height=_START_SIZE, dither=True,
                                uni=self._screen.unicode_aware),
                True]
            if len(self._tiles) > _CACHE_SIZE:
                self._tiles.popitem(False)
            self._screen.force_update()

    def _get_vector_tile(self, x_tile, y_tile, z_tile):
        """Load up a single vector tile."""
        cache_file = "mapscache/{}.{}.{}.json".format(z_tile, x_tile, y_tile)
        if cache_file not in self._tiles:
            if os.path.isfile(cache_file):
                with open(cache_file, 'rb') as f:
                    tile = json.loads(f.read().decode('utf-8'))
            else:
                url = _VECTOR_URL.format(z_tile, x_tile, y_tile, _KEY)
                data = requests.get(url).content
                try:
                    tile = mapbox_vector_tile.decode(data)
                    with open(cache_file, mode='w') as f:
                        json.dump(literal_eval(repr(tile)), f)
                except DecodeError:
                    tile = None
            if tile:
                self._tiles[cache_file] = [x_tile, y_tile, z_tile, tile, False]
                if len(self._tiles) > _CACHE_SIZE:
                    self._tiles.popitem(False)
                self._screen.force_update()

    def _get_tiles(self):
        """Background thread to download map tiles as required."""
        while self._running:
            self._updated.wait()
            self._updated.clear()

            # Save off current view and find the nearest tile.
            satellite = self._satellite
            zoom = self._zoom
            size = self._size
            n = 2 ** zoom
            x_offset = self._convert_longitude(self._longitude)
            y_offset = self._convert_latitude(self._latitude)

            # Get the visible tiles around that location - getting most relevant first
            for x, y, z in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0),
                            (0, 0, -1), (0, 0, 1),
                            (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)]:
                # Restart if we've already zoomed to another level
                if self._zoom != zoom:
                    break

                # Don't get tile if it falls off the grid
                x_tile = int(x_offset // size) + x
                y_tile = int(y_offset // size) + y
                z_tile = zoom + z
                if (x_tile < 0 or x_tile >= n or y_tile < 0 or y_tile >= n or
                        z_tile < 0 or z_tile > 20):
                    continue
                # noinspection PyBroadException
                try:

                    # Don't bother rendering if the tile is not visible
                    top = y_tile * size - y_offset + self._screen.height // 2
                    left = (x_tile * size - x_offset + self._screen.width // 4) * 2
                    if z == 0 and (left > self._screen.width or left + self._size * 2 < 0 or
                                   top > self._screen.height or top + self._size < 0):
                        continue

                    if satellite:
                        self._get_satellite_tile(x_tile, y_tile, z_tile)
                    else:
                        self._get_vector_tile(x_tile, y_tile, z_tile)
                # pylint: disable=broad-except
                except Exception:
                    self._oops = "{} - tile loc: {} {} {}".format(
                        traceback.format_exc(), x_tile, y_tile, z_tile)

                # Generally refresh screen after we've downloaded everything
                self._screen.force_update()

    def _get_features(self):
        """Decide which layers to render based on current zoom level and view type."""
        if self._satellite:
            return [("water", [], [])]
        elif self._zoom <= 2:
            return [
                ("water", [], []),
                ("marine_label", [], [1]),
            ]
        elif self._zoom <= 7:
            return [
                ("admin", [], []),
                ("water", [], []),
                ("road", ["motorway"], []),
                ("country_label", [], []),
                ("marine_label", [], [1]),
                ("state_label", [], []),
                ("place_label", [], ["city", "town"]),
            ]
        elif self._zoom <= 10:
            return [
                ("admin", [], []),
                ("water", [], []),
                ("road", ["motorway", "motorway_link", "trunk"], []),
                ("country_label", [], []),
                ("marine_label", [], [1]),
                ("state_label", [], []),
                ("place_label", [], ["city", "town"]),
            ]
        else:
            return [
                ("landuse", ["agriculture", "grass", "park"], []),
                ("water", [], []),
                ("waterway", ["river", "canal"], []),
                ("building", [], []),
                ("road",
                 ["motorway", "motorway_link", "trunk", "primary", "secondary"]
                 if self._zoom <= 14 else
                 ["motorway", "motorway_link", "trunk", "primary", "secondary", "tertiary",
                  "link", "street", "tunnel"],
                 []),
                ("poi_label", [], []),
            ]

    def _draw_lines_internal(self, coords, colour, bg):
        """Helper to draw lines connecting a set of nodes that are scaled for the Screen."""
        for i, (x, y) in enumerate(coords):
            if i == 0:
                self._screen.move(x, y)
            else:
                self._screen.draw(x, y, colour=colour, bg=bg, thin=True)

    def _draw_polygons(self, feature, bg, colour, extent, polygons, xo, yo):
        """Draw a set of polygons from a vector tile."""
        coords = []
        for polygon in polygons:
            coords.append([self._scale_coords(x, y, extent, xo, yo) for x, y in polygon])
        # Polygons are expensive to draw and the buildings layer is huge - so we convert to
        # lines in order to process updates fast enough to animate.
        if "type" in feature["properties"] and "building" in feature["properties"]["type"]:
            for line in coords:
                self._draw_lines_internal(line, colour, bg)
        else:
            self._screen.fill_polygon(coords, colour=colour, bg=bg)

    def _draw_lines(self, bg, colour, extent, line, xo, yo):
        """Draw a set of lines from a vector tile."""
        coords = [self._scale_coords(x, y, extent, xo, yo) for x, y in line]
        self._draw_lines_internal(coords, colour, bg)

    def _draw_feature(self, feature, extent, colour, bg, xo, yo):
        """Draw a single feature from a layer in a vector tile."""
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            self._draw_polygons(feature, bg, colour, extent, geometry["coordinates"], xo, yo)
        elif feature["geometry"]["type"] == "MultiPolygon":
            for multi_polygon in geometry["coordinates"]:
                self._draw_polygons(feature, bg, colour, extent, multi_polygon, xo, yo)
        elif feature["geometry"]["type"] == "LineString":
            self._draw_lines(bg, colour, extent, geometry["coordinates"], xo, yo)
        elif feature["geometry"]["type"] == "MultiLineString":
            for line in geometry["coordinates"]:
                self._draw_lines(bg, colour, extent, line, xo, yo)
        elif feature["geometry"]["type"] == "Point":
            x, y = self._scale_coords(
                geometry["coordinates"][0], geometry["coordinates"][1], extent, xo, yo)
            text = u" {} ".format(feature["properties"]["name_en"])
            self._screen.print_at(text, int(x - len(text) / 2), int(y), colour=colour, bg=bg)

    def _draw_tile_layer(self, tile, layer_name, c_filters, colour, t_filters, x, y, bg):
        """Draw the visible geometry in the specified map tile."""
        # Don't bother rendering if the tile is not visible
        left = (x + self._screen.width // 4) * 2
        top = y + self._screen.height // 2
        if (left > self._screen.width or left + self._size * 2 < 0 or
                top > self._screen.height or top + self._size < 0):
            return 0

        # Not all layers are available in every tile.
        try:
            _layer = tile[layer_name]
            _extent = float(_layer["extent"])
        except KeyError:
            return 0

        for _feature in _layer["features"]:
            try:
                if c_filters and _feature["properties"]["class"] not in c_filters:
                    continue
                if (t_filters and _feature["type"] not in t_filters and
                        _feature["properties"]["type"] not in t_filters):
                    continue
                self._draw_feature(
                    _feature, _extent, colour, bg,
                    (x + self._screen.width // 4) * 2, y + self._screen.height // 2)
            except KeyError:
                pass
        return 1

    def _draw_satellite_tile(self, tile, x, y):
        """Draw a satellite image tile to screen."""
        image, colours = tile.rendered_text
        for (i, line) in enumerate(image):
            self._screen.paint(line, x, y + i, colour_map=colours[i])
        return 1

    def _draw_tiles(self, x_offset, y_offset, bg):
        """Render all visible tiles a layer at a time."""
        count = 0
        for layer_name, c_filters, t_filters in self._get_features():
            colour = (self._256_PALETTE[layer_name]
                      if self._screen.colours >= 256 else self._16_PALETTE[layer_name])
            for x, y, z, tile, satellite in sorted(self._tiles.values(), key=lambda k: k[0]):
                # Don't draw the wrong type or zoom of tile.
                if satellite != self._satellite or z != self._zoom:
                    continue

                # Convert tile location into pixels and draw the tile.
                x *= self._size
                y *= self._size
                if satellite:
                    count += self._draw_satellite_tile(
                        tile,
                        int((x-x_offset + self._screen.width // 4) * 2),
                        int(y-y_offset + self._screen.height // 2))
                else:
                    count += self._draw_tile_layer(tile, layer_name, c_filters, colour, t_filters,
                                                   x - x_offset, y - y_offset, bg)
        return count

    def _zoom_map(self, zoom_out=True):
        """Animate the zoom in/out as appropriate for the displayed map tile."""
        size_step = 1 / _ZOOM_STEP if zoom_out else _ZOOM_STEP
        self._next_update = 1
        if self._satellite:
            size_step **= _ZOOM_ANIMATION_STEPS
        self._size *= size_step
        if self._size <= _ZOOM_OUT_SIZE:
            if self._zoom > 0:
                self._zoom -= 1
                self._size = _START_SIZE
            else:
                self._size = _ZOOM_OUT_SIZE
        elif self._size >= _ZOOM_IN_SIZE:
            if self._zoom < 20:
                self._zoom += 1
                self._size = _START_SIZE
            else:
                self._size = _ZOOM_IN_SIZE

    def _move_to_desired_location(self):
        """Animate movement to desired location on map."""
        self._next_update = 100000
        x_start = self._convert_longitude(self._longitude)
        y_start = self._convert_latitude(self._latitude)
        x_end = self._convert_longitude(self._desired_longitude)
        y_end = self._convert_latitude(self._desired_latitude)
        if sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2) > _START_SIZE // 4:
            self._zoom_map(True)
        elif self._zoom != self._desired_zoom:
            self._zoom_map(self._desired_zoom < self._zoom)
        if self._longitude != self._desired_longitude:
            self._next_update = 1
            if self._desired_longitude < self._longitude:
                self._longitude = max(self._longitude - 360 / 2 ** self._zoom / self._size * 2,
                                      self._desired_longitude)
            else:
                self._longitude = min(self._longitude + 360 / 2 ** self._zoom / self._size * 2,
                                      self._desired_longitude)
        if self._latitude != self._desired_latitude:
            self._next_update = 1
            if self._desired_latitude < self._latitude:
                self._latitude = max(self._inc_lat(self._latitude, 2), self._desired_latitude)
            else:
                self._latitude = min(self._inc_lat(self._latitude, -2), self._desired_latitude)
        if self._next_update == 1:
            self._updated.set()

    def _update(self, frame_no):
        """Draw the latest set of tiles to the Screen."""
        # Check for any fatal errors from the background thread and quit if we hit anything.
        if self._oops:
            raise RuntimeError(self._oops)

        # Calculate new positions for animated movement.
        self._move_to_desired_location()

        # Re-draw the tiles - if we have any suitable ones downloaded.
        count = 0
        x_offset = self._convert_longitude(self._longitude)
        y_offset = self._convert_latitude(self._latitude)
        if self._tiles:
            # Clear the area first.
            bg = 253 if self._screen.unicode_aware and self._screen.colours >= 256 else 0
            for y in range(self._screen.height):
                self._screen.print_at("." * self._screen.width, 0, y, colour=bg, bg=bg)

            # Now draw all the available tiles.
            count = self._draw_tiles(x_offset, y_offset, bg)

        # Just a few pointers on what the user should do...
        if count == 0:
            self._screen.centre(" Loading - please wait... ", self._screen.height // 2, 1)

        self._screen.centre("Press '?' for help.", 0, 1)
        if _KEY == "":
            footer = "Using local cached data - go to https://www.mapbox.com/ and get a free key."
        else:
            footer = u"Zoom: {} Location: {:.6}, {:.6} Maps: © Mapbox, © OpenStreetMap".format(
                self._zoom, self._longitude, self._latitude)
        self._screen.centre(footer, self._screen.height - 1, 1)

        return count

    def process_event(self, event):
        """User input for the main map view."""
        if isinstance(event, KeyboardEvent):
            if event.key_code in [Screen.ctrl("m"), Screen.ctrl("j")]:
                self._scene.add_effect(
                    EnterLocation(
                        self._screen, self._longitude, self._latitude, self._on_new_location))
            elif event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")
            elif event.key_code in [ord('t'), ord('T')]:
                self._satellite = not self._satellite
                if self._satellite:
                    self._size = _START_SIZE
            elif event.key_code == ord("?"):
                self._scene.add_effect(PopUpDialog(self._screen, _HELP, ["OK"]))
            elif event.key_code == ord("+") and self._zoom <= 20:
                if self._desired_zoom < 20:
                    self._desired_zoom += 1
            elif event.key_code == ord("-") and self._zoom >= 0:
                if self._desired_zoom > 0:
                    self._desired_zoom -= 1
            elif event.key_code == ord("0"):
                self._desired_zoom = 0
            elif event.key_code == ord("9"):
                self._desired_zoom = 20
            elif event.key_code == Screen.KEY_LEFT:
                self._desired_longitude -= 360 / 2 ** self._zoom / self._size * 10
            elif event.key_code == Screen.KEY_RIGHT:
                self._desired_longitude += 360 / 2 ** self._zoom / self._size * 10
            elif event.key_code == Screen.KEY_UP:
                self._desired_latitude = self._inc_lat(self._desired_latitude, -self._size / 10)
            elif event.key_code == Screen.KEY_DOWN:
                self._desired_latitude = self._inc_lat(self._desired_latitude, self._size / 10)
            else:
                return

            # Trigger a reload of the tiles and redraw map
            self._updated.set()
            self._screen.force_update()

    def _on_new_location(self, form):
        """Set a new desired location entered in the pop-up form."""
        self._desired_longitude = float(form.data["long"])
        self._desired_latitude = float(form.data["lat"])
        self._desired_zoom = 13
        self._screen.force_update()

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def clone(self, new_screen, new_scene):
        # On resize, there will be a new Map - kill the thread in this one.
        self._running = False
        self._updated.set()

    @property
    def frame_update_count(self):
        # Only redraw if required - as determined by the update logic.
        return self._next_update

    @property
    def stop_frame(self):
        # No specific end point for this Effect.  Carry on running forever.
        return 0

    def reset(self):
        # Nothing special to do.  Just need this to satisfy the ABC.
        pass


def demo(screen, scene):
    screen.play([Scene([Map(screen)], -1)], stop_on_resize=True, start_scene=scene)


if __name__ == "__main__":
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/kaleidoscope.py
from math import sqrt

from asciimatics.renderers import Kaleidoscope, FigletText, Rainbow, RotatedDuplicate, \
    StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    scenes = []
    cell1 = Rainbow(screen,
                    RotatedDuplicate(screen.width // 2,
                                     max(screen.width // 2, screen.height),
                                     FigletText("ASCII" if screen.width < 80 else "ASCII rules",
                                                font="banner",
                                                width=screen.width // 2)))
    cell2 = ""
    size = int(sqrt(screen.height ** 2 + screen.width ** 2 // 4))
    for _ in range(size):
        for x in range(size):
            c = x * screen.colours // size
            cell2 += "${%d,2,%d}:" % (c, c)
        cell2 += "\n"
    for i in range(8):
        scenes.append(
            Scene([Print(screen,
                         Kaleidoscope(screen.height, screen.width, cell1, i),
                         0,
                         speed=1,
                         transparent=False),
                   Print(screen,
                         FigletText(str(i)), screen.height - 6, x=screen.width - 8, speed=1)],
                  duration=360))
        scenes.append(
            Scene([Print(screen,
                         Kaleidoscope(screen.height, screen.width, StaticRenderer([cell2]), i),
                         0,
                         speed=1,
                         transparent=False)],
                  duration=360))
    screen.play(scenes, stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
        
'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/frame_borders.py
# NOT WORKING (2 Feb 2022)
#from asciimatics.constants import DOUBLE_LINE
from asciimatics.widgets import Frame, Text, TextBox, Layout, Label, Button, PopUpDialog, Widget
from asciimatics.effects import Background
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
#from asciimatics.utilities import BoxTool


class TopFrame(Frame):
    def __init__(self, screen):
        super(TopFrame, self).__init__(screen,
                                       int(screen.height // 3) - 1,
                                       screen.width // 2,
                                       y=0,
                                       has_border=True,
                                       can_scroll=True,
                                       name="Top Form")
        self.border_box.style = 2 #DOUBLE_LINE
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(Label("Scrolling, with border"), 1)
        for i in range(screen.height // 2):
            layout.add_widget(Text(label=f"Text {i}:"), 1)
        self.fix()


class MidFrame(Frame):
    def __init__(self, screen):
        super(MidFrame, self).__init__(screen,
                                       int(screen.height // 3) - 1,
                                       screen.width // 2,
                                       y=int(screen.height // 3),
                                       has_border=False,
                                       can_scroll=True,
                                       name="Mid Form")
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(Label("Scrolling, no border"), 1)
        for i in range(screen.height // 2):
            layout.add_widget(Text(label=f"Text {i}:"), 1)
        self.fix()


class BottomFrame(Frame):
    def __init__(self, screen):
        super(BottomFrame, self).__init__(screen,
                                          int(screen.height // 3),
                                          screen.width // 2,
                                          y=int(screen.height * 2 // 3),
                                          has_border=False,
                                          can_scroll=False,
                                          name="Bottom Form")
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(Label("No scrolling, no border"), 1)
        layout.add_widget(TextBox(Widget.FILL_FRAME, label="Box 3:", name="BOX3"), 1)
        layout.add_widget(Text(label="Text 3:", name="TEXT3"), 1)
        layout.add_widget(Button("Quit", self._quit, label="To exit:"), 1)
        self.fix()

    def _quit(self):
        popup = PopUpDialog(self._screen, "Are you sure?", ["Yes", "No"],
                    has_shadow=True, on_close=self._quit_on_yes)
        self._scene.add_effect(popup)

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


def demo(screen, scene):
    scenes = [Scene([
        Background(screen),
        TopFrame(screen),
        MidFrame(screen),
        BottomFrame(screen),
    ], -1)]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            quit()
        except ResizeScreenError as e:
            last_scene = e.scene
'''
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/forms.py
from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Text, \
    CheckBox, RadioButtons, Button, PopUpDialog, TimePicker, DatePicker, DropdownList, PopupMenu
from asciimatics.effects import Background
from asciimatics.event import MouseEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
from asciimatics.parsers import AsciimaticsParser
import sys
import re
import datetime
import logging

# Test data
tree = r"""
       ${3,1}*
${2}      / \
${2}     /${1}o${2}  \
${2}    /_   _\
${2}     /   \${4}b
${2}    /     \
${2}   /   ${1}o${2}   \
${2}  /__     __\
  ${1}d${2} / ${4}o${2}   \
${2}   /       \
${2}  / ${4}o     ${1}o${2}.\
${2} /___________\
      ${3}|||
      ${3}|||
""".split("\n")

# Initial data for the form
form_data = {
    "TA": tree,
    "TB": "alphabet",
    "TC": "123",
    "TD": "a@b.com",
    "RO": "You can't touch this",
    "Things": 2,
    "CA": False,
    "CB": True,
    "CC": False,
    "DATE": datetime.datetime.now().date(),
    "TIME": datetime.datetime.now().time(),
    "PWD": "",
    "DD": 1
}

logging.basicConfig(filename="forms.log", level=logging.DEBUG)


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen,
                                        int(screen.height * 2 // 3),
                                        int(screen.width * 2 // 3),
                                        data=form_data,
                                        has_shadow=True,
                                        name="My Form")
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        self._reset_button = Button("Reset", self._reset)
        layout.add_widget(Label("Group 1:"), 1)
        layout.add_widget(TextBox(5,
                                  label="My First Box:",
                                  name="TA",
                                  parser=AsciimaticsParser(),
                                  line_wrap=True,
                                  on_change=self._on_change), 1)
        layout.add_widget(
            Text(label="Alpha:",
                 name="TB",
                 on_change=self._on_change,
                 validator="^[a-zA-Z]*$"), 1)
        layout.add_widget(
            Text(label="Number:",
                 name="TC",
                 on_change=self._on_change,
                 validator="^[0-9]*$",
                 max_length=4), 1)
        layout.add_widget(
            Text(label="Email:",
                 name="TD",
                 on_change=self._on_change,
                 validator=self._check_email), 1)
        layout.add_widget(Text(label="Readonly:", name="RO", readonly=True), 1)
        layout.add_widget(Divider(height=2), 1)
        layout.add_widget(Label("Group 2:"), 1)
        layout.add_widget(RadioButtons([("Option 1", 1),
                                        ("Option 2", 2),
                                        ("Option 3", 3)],
                                       label="A Longer Selection:",
                                       name="Things",
                                       on_change=self._on_change), 1)
        layout.add_widget(CheckBox("Field 1",
                                   label="A very silly long name for fields:",
                                   name="CA",
                                   on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 2", name="CB", on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 3", name="CC", on_change=self._on_change), 1)
        layout.add_widget(DatePicker("Date",
                                     name="DATE",
                                     year_range=range(1999, 2100),
                                     on_change=self._on_change), 1)
        layout.add_widget(
            TimePicker("Time", name="TIME", on_change=self._on_change, seconds=True), 1)
        layout.add_widget(Text("Password", name="PWD", on_change=self._on_change, hide_char="*"), 1)
        layout.add_widget(DropdownList(
            [("Item 1", 1),
             ("Item 2", 2),
             ("Item 3", 3),
             ("Item 3", 4),
             ("Item 3", 5),
             ("Item 3", 6),
             ("Item 3", 7),
             ("Item 3", 8),
             ("Item 3", 9),
             ("Item 3", 10),
             ("Item 3", 11),
             ("Item 3", 12),
             ("Item 3", 13),
             ("Item 3", 14),
             ("Item 3", 15),
             ("Item 3", 16),
             ("Item 4", 17),
             ("Item 5", 18), ],
            label="Dropdown", name="DD", on_change=self._on_change), 1)
        layout.add_widget(Divider(height=3), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def process_event(self, event):
        # Handle dynamic pop-ups now.
        if (event is not None and isinstance(event, MouseEvent) and
                event.buttons == MouseEvent.DOUBLE_CLICK):
            # By processing the double-click before Frame handling, we have absolute coordinates.
            options = [
                ("Default", self._set_default),
                ("Green", self._set_green),
                ("Monochrome", self._set_mono),
                ("Bright", self._set_bright),
            ]
            if self.screen.colours >= 256:
                options.append(("Red/white", self._set_tlj))
            self._scene.add_effect(PopupMenu(self.screen, options, event.x, event.y))
            event = None

        # Pass any other event on to the Frame and contained widgets.
        return super(DemoFrame, self).process_event(event)

    def _set_default(self):
        self.set_theme("default")

    def _set_green(self):
        self.set_theme("green")

    def _set_mono(self):
        self.set_theme("monochrome")

    def _set_bright(self):
        self.set_theme("bright")

    def _set_tlj(self):
        self.set_theme("tlj256")

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in form_data or form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        has_shadow=True,
                        on_close=self._quit_on_yes))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


def demo(screen, scene):
    screen.play([Scene([
        Background(screen),
        DemoFrame(screen)
    ], -1)], stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        
'''        
        
"""https://github.com/peterbrittain/asciimatics/blob/master/samples/fireworks.py
from asciimatics.effects import Stars, Print
from asciimatics.particles import RingFirework, SerpentFirework, StarFirework, \
    PalmFirework
from asciimatics.renderers import SpeechBubble, FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from random import randint, choice
import sys


def demo(screen):
    scenes = []
    effects = [
        Stars(screen, screen.width),
        
        Print(screen,
              SpeechBubble("Press space to see it again"),
              y=screen.height - 3,
              start_frame=300)
        
    ]
    for _ in range(20):
        fireworks = [
            (PalmFirework, 25, 30),
            (PalmFirework, 25, 30),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (RingFirework, 20, 30),
            (SerpentFirework, 30, 35),
        ]
        firework, start, stop = choice(fireworks)
        effects.insert(
            1,
            firework(screen,
                     randint(0, screen.width),
                     randint(screen.height // 8, screen.height * 3 // 4),
                     randint(start, stop),
                     start_frame=randint(0, 250)))
    '''
    effects.append(Print(screen,
                         Rainbow(screen, FigletText("HAPPY")),
                         screen.height // 2 - 6,
                         speed=1,
                         start_frame=100))
    effects.append(Print(screen,
                         Rainbow(screen, FigletText("NEW YEAR!")),
                         screen.height // 2 + 1,
                         speed=1,
                         start_frame=100))
    '''
    scenes.append(Scene(effects, -1))
    

    screen.play(scenes, stop_on_resize=True)


while True:
    try:
        Screen.wrapper(demo)
        sys.exit(0)
    except ResizeScreenError:
        pass
"""

"""https://github.com/peterbrittain/asciimatics/blob/master/samples/experimental.py
import re

from asciimatics.effects import Julia, Clock
from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Text, \
    CheckBox, RadioButtons, Button, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
import sys

# Initial data for the form
form_data = {
    "TA": ["Hello world!", "How are you?"],
    "TB": "alphabet",
    "TC": "123",
    "TD": "a@b.com",
    "Things": 2,
    "CA": False,
    "CB": True,
    "CC": False,
}


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen,
                                        int(screen.height * 2 // 3),
                                        int(screen.width * 2 // 3),
                                        data=form_data,
                                        has_shadow=True,
                                        name="My Form")
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        self._reset_button = Button("Reset", self._reset)
        layout.add_widget(Label("Group 1:"), 1)
        layout.add_widget(TextBox(5,
                                  label="My First Box:",
                                  name="TA",
                                  on_change=self._on_change), 1)
        layout.add_widget(
            Text(label="Alpha:",
                 name="TB",
                 on_change=self._on_change,
                 validator="^[a-zA-Z]*$"), 1)
        layout.add_widget(
            Text(label="Number:",
                 name="TC",
                 on_change=self._on_change,
                 validator="^[0-9]*$"), 1)
        layout.add_widget(
            Text(label="Email:",
                 name="TD",
                 on_change=self._on_change,
                 validator=self._check_email), 1)
        layout.add_widget(Divider(height=2), 1)
        layout.add_widget(Label("Group 2:"), 1)
        layout.add_widget(RadioButtons([("Option 1", 1),
                                        ("Option 2", 2),
                                        ("Option 3", 3)],
                                       label="A Longer Selection:",
                                       name="Things",
                                       on_change=self._on_change), 1)
        layout.add_widget(CheckBox("Field 1",
                                   label="A very silly long name for fields:",
                                   name="CA",
                                   on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 2", name="CB", on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 3", name="CC", on_change=self._on_change), 1)
        layout.add_widget(Divider(height=3), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in form_data or form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


class ClockFrame(Frame):
    def __init__(self, screen, x, y):
        super(ClockFrame, self).__init__(screen, 13, 26,
                                         name="Clock",
                                         has_shadow=True,
                                         x=x, y=y)
        self.add_effect(Clock(self._canvas, 13, 7, 7, Screen.COLOUR_BLUE))
        self.fix()


def demo(screen, scene):
    scenes = []
    effects = [
        Julia(screen),
        ClockFrame(screen, 0, 0),
        ClockFrame(screen, screen.width - 26, 0),
        ClockFrame(screen, 0, screen.height - 13),
        ClockFrame(screen, screen.width - 26, screen.height - 13),
        DemoFrame(screen),
    ]
    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

"""

"""https://github.com/peterbrittain/asciimatics/blob/master/samples/contact_list.py
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3


class ContactModel(object):
    def __init__(self):
        # Create a database in RAM.
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self._db.cursor().execute('''
            CREATE TABLE contacts(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                notes TEXT)
        ''')
        self._db.commit()

        # Current contact when editing.
        self.current_id = None

    def add(self, contact):
        self._db.cursor().execute('''
            INSERT INTO contacts(name, phone, address, email, notes)
            VALUES(:name, :phone, :address, :email, :notes)''',
                                  contact)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from contacts").fetchall()

    def get_contact(self, contact_id):
        return self._db.cursor().execute(
            "SELECT * from contacts WHERE id=:id", {"id": contact_id}).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE contacts SET name=:name, phone=:phone, address=:address,
                email=:email, notes=:notes WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_contact(self, contact_id):
        self._db.cursor().execute('''
            DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
        self._db.commit()


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Contact List")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="contacts",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["contacts"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


def demo(screen, scene):
    scenes = [
        Scene([ListView(screen, contacts)], -1, name="Main"),
        Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = ContactModel()
last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
            
"""

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/cogs.py
from __future__ import division
from asciimatics.effects import Cog, Print
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    # Typical terminals are 80x24 on UNIX and 80x25 on Windows
    if screen.width != 80 or screen.height not in (24, 25):
        effects = [
            Print(screen, FigletText("Resize to 80x24"),
                  y=screen.height//2-3),
        ]
    else:
        effects = [
            Cog(screen, 20, 10, 10),
            Cog(screen, 60, 30, 15, direction=-1),
            Print(screen, FigletText("ascii", font="smkeyboard"),
                  attr=Screen.A_BOLD, x=47, y=3, start_frame=50),
            Print(screen, FigletText("matics", font="smkeyboard"),
                  attr=Screen.A_BOLD, x=45, y=7, start_frame=100),
            Print(screen, FigletText("by Peter Brittain", font="term"),
                  x=8, y=22, start_frame=150)
        ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/bg_colours.py
from __future__ import division
from asciimatics.effects import Wipe, Print
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    scenes = []

    for bg, name in [
            (Screen.COLOUR_DEFAULT, "DEFAULT"),
            (Screen.COLOUR_RED, "RED"),
            (Screen.COLOUR_YELLOW, "YELLOW"),
            (Screen.COLOUR_GREEN, "GREEN"),
            (Screen.COLOUR_CYAN, "CYAN"),
            (Screen.COLOUR_BLUE, "BLUE"),
            (Screen.COLOUR_MAGENTA, "MAGENTA"),
            (Screen.COLOUR_WHITE, "WHITE")]:
        effects = [
            Wipe(screen, bg=bg, stop_frame=screen.height * 2 + 30),
            Print(screen, FigletText(name, "epic"), screen.height // 2 - 4,
                  colour=bg if bg == Screen.COLOUR_DEFAULT else 7 - bg,
                  bg=bg,
                  start_frame=screen.height * 2),
            Print(screen,
                  SpeechBubble("Testing background colours - press X to exit"),
                  screen.height-5,
                  speed=1, transparent=False)
        ]
        scenes.append(Scene(effects, 0, clear=False))

    screen.play(scenes, stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''        
        
''' https://github.com/peterbrittain/asciimatics/blob/master/samples/basics.py
from __future__ import division
from builtins import range
import copy
import math
from asciimatics.effects import Cycle, Print, Stars
from asciimatics.renderers import SpeechBubble, FigletText, Box
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import Path
from asciimatics.exceptions import ResizeScreenError
import sys


def _speak(screen, text, pos, start):
    return Print(
        screen,
        SpeechBubble(text, "L", uni=screen.unicode_aware),
        x=pos[0] + 4, y=pos[1] - 4,
        colour=Screen.COLOUR_CYAN,
        clear=True,
        start_frame=start,
        stop_frame=start+50)


def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)
    podium = (8, 5)

    # Scene 1.
    path = Path()
    path.jump_to(-20, centre[1])
    path.move_straight_to(centre[0], centre[1], 10)
    path.wait(30)
    path.move_straight_to(podium[0], podium[1], 10)
    path.wait(100)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "WELCOME TO ASCIIMATICS", centre, 30),
        _speak(screen, "My name is Aristotle Arrow.", podium, 110),
        _speak(screen,
               "I'm here to help you learn ASCIImatics.", podium, 180),
    ]
    scenes.append(Scene(effects))

    # Scene 2.
    path = Path()
    path.jump_to(podium[0], podium[1])

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "Let's start with the Screen...", podium, 10),
        _speak(screen, "This is your Screen object.", podium, 80),
        Print(screen,
              Box(screen.width, screen.height, uni=screen.unicode_aware),
              0, 0, start_frame=90),
        _speak(screen, "It lets you play a Scene like this one I'm in.",
               podium, 150),
        _speak(screen, "A Scene contains one or more Effects.", podium, 220),
        _speak(screen, "Like me - I'm a Sprite!", podium, 290),
        _speak(screen, "Or these Stars.", podium, 360),
        _speak(screen, "As you can see, the Screen handles them both at once.",
               podium, 430),
        _speak(screen, "It can handle as many Effects as you like.",
               podium, 500),
        _speak(screen, "Please press <SPACE> now.", podium, 570),
        Stars(screen, (screen.width + screen.height) // 2, start_frame=360)
    ]
    scenes.append(Scene(effects, -1))

    # Scene 3.
    path = Path()
    path.jump_to(podium[0], podium[1])

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "This is a new Scene.", podium, 10),
        _speak(screen, "The Screen stops all Effects and clears itself between "
                       "Scenes.",
               podium, 70),
        _speak(screen, "That's why you can't see the Stars now.", podium, 130),
        _speak(screen, "(Though you can override that if you need to.)", podium,
               200),
        _speak(screen, "Please press <SPACE> now.", podium, 270),
    ]
    scenes.append(Scene(effects, -1))

    # Scene 4.
    path = Path()
    path.jump_to(podium[0], podium[1])

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "So, how do you design your animation?", podium, 10),
        _speak(screen, "1) Decide on your cinematic flow of Scenes.", podium,
               80),
        _speak(screen, "2) Create the Effects in each Scene.", podium, 150),
        _speak(screen, "3) Pass the Scenes to the Screen to play.", podium,
               220),
        _speak(screen, "It really is that easy!", podium, 290),
        _speak(screen, "Just look at this sample code.", podium, 360),
        _speak(screen, "Please press <SPACE> now.", podium, 430),
    ]
    scenes.append(Scene(effects, -1))

    # Scene 5.
    path = Path()
    path.jump_to(podium[0], podium[1])

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "There are various effects you can use.  For "
                       "example...",
               podium, 10),
        Cycle(screen,
              FigletText("Colour cycling"),
              centre[1] - 5,
              start_frame=100),
        Cycle(screen,
              FigletText("using Figlet"),
              centre[1] + 1,
              start_frame=100),
        _speak(screen, "Look in the effects module for more...",
               podium, 290),
        _speak(screen, "Please press <SPACE> now.", podium, 360),
    ]
    scenes.append(Scene(effects, -1))

    # Scene 6.
    path = Path()
    path.jump_to(podium[0], podium[1])
    curve_path = []
    for i in range(0, 11):
        curve_path.append(
            (centre[0] + (screen.width / 4 * math.sin(i * math.pi / 5)),
             centre[1] - (screen.height / 4 * math.cos(i * math.pi / 5))))
    path2 = Path()
    path2.jump_to(centre[0], centre[1] - screen.height // 4)
    path2.move_round_to(curve_path, 60)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "Sprites (like me) are also an Effect.", podium, 10),
        _speak(screen, "We take a pre-defined Path to follow.", podium, 80),
        _speak(screen, "Like this one...", podium, 150),
        Plot(screen, path2, colour=Screen.COLOUR_BLUE, start_frame=160,
             stop_frame=300),
        _speak(screen, "My friend Sam will now follow it...", podium, 320),
        Sam(screen, copy.copy(path2), start_frame=380),
        _speak(screen, "Please press <SPACE> now.", podium, 420),
    ]
    scenes.append(Scene(effects, -1))

    # Scene 7.
    path = Path()
    path.jump_to(podium[0], podium[1])
    path.wait(60)
    path.move_straight_to(-5, podium[1], 20)
    path.wait(300)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "Goodbye!", podium, 10),
        Cycle(screen,
              FigletText("THE END!"),
              centre[1] - 4,
              start_frame=100),
        Print(screen, SpeechBubble("Press X to exit"), centre[1] + 6,
              start_frame=150)
    ]
    scenes.append(Scene(effects, 500))

    screen.play(scenes, stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass

'''


'''https://github.com/peterbrittain/asciimatics/blob/v1.13/samples/bars.py
from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import math
import time
from random import randint


def fn():
    return randint(0, 40)


def wv(x):
    return lambda: 1 + math.sin(math.pi * (2*time.time()+x) / 5)


def demo(screen):
    scenes = []
    if screen.width != 132 or screen.height != 24:
        effects = [
            Print(screen, FigletText("Resize to 132x24"),
                  y=screen.height//2-3),
        ]
    else:
        effects = [
            Print(screen,
                  BarChart(10, 40, [fn, fn],
                           char="=",
                           gradient=[(20, Screen.COLOUR_GREEN),
                                     (30, Screen.COLOUR_YELLOW),
                                     (40, Screen.COLOUR_RED)]),
                  x=13, y=1, transparent=False, speed=2),
            Print(screen,
                  BarChart(
                      13, 60,
                      [wv(1), wv(2), wv(3), wv(4), wv(5), wv(7), wv(8), wv(9)],
                      colour=Screen.COLOUR_GREEN,
                      axes=BarChart.BOTH,
                      scale=2.0),
                  x=68, y=1, transparent=False, speed=2),
            Print(screen,
                  BarChart(
                      7, 60, [lambda: time.time() * 10 % 101],
                      gradient=[
                          (33, Screen.COLOUR_RED, Screen.COLOUR_RED),
                          (66, Screen.COLOUR_YELLOW, Screen.COLOUR_YELLOW),
                          (100, Screen.COLOUR_WHITE, Screen.COLOUR_WHITE),
                      ] if screen.colours < 256 else [
                          (10, 234, 234), (20, 236, 236), (30, 238, 238),
                          (40, 240, 240), (50, 242, 242), (60, 244, 244),
                          (70, 246, 246), (80, 248, 248), (90, 250, 250),
                          (100, 252, 252)
                      ],
                      char=">",
                      scale=100.0,
                      labels=True,
                      axes=BarChart.X_AXIS),
                  x=68, y=16, transparent=False, speed=2),
            Print(screen,
                  BarChart(
                      10, 60,
                      [wv(1), wv(2), wv(3), wv(4), wv(5), wv(7), wv(8), wv(9)],
                      colour=[c for c in range(1, 8)],
                      bg=[c for c in range(1, 8)],
                      scale=2.0,
                      axes=BarChart.X_AXIS,
                      intervals=0.5,
                      labels=True,
                      border=False),
                  x=3, y=13, transparent=False, speed=2)
        ]

    scenes.append(Scene(effects, -1))
    screen.play(scenes, stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''    
    
'''https://github.com/peterbrittain/asciimatics/blob/v1.13/samples/256colour.py
from __future__ import division
from asciimatics.effects import Print, Clock
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    effects = [
        Print(screen, Rainbow(screen, FigletText("256 colours")),
              y=screen.height//2 - 8),
        Print(screen, Rainbow(screen, FigletText("for xterm users")),
              y=screen.height//2 + 3),
        Clock(screen, screen.width//2, screen.height//2, screen.height//2),
    ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)

def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''