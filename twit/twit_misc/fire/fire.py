#!/usr/bin/env python3

# TAP-DEMO
# RAY-CASTING
# PLASMA
# JULIA FRACTAL
# INTERACTIVE
# ASCII IMAGE RENDERING

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/fire.py'''
from asciimatics.renderers import FigletText, Fire
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from pyfiglet import Figlet
import sys


def demo(screen):
    scenes = []

    effects = [
        Print(screen,
              Fire(screen.height, 80, "*" * 70, 0.8, 60, screen.colours,
                   bg=screen.colours >= 256),
              0,
              speed=1,
              transparent=False),
        Print(screen,
              FigletText("Help!", "banner3"),
              (screen.height - 4) // 2,
              colour=Screen.COLOUR_BLACK,
              speed=1,
              stop_frame=30),
        Print(screen,
              FigletText("I'm", "banner3"),
              (screen.height - 4) // 2,
              colour=Screen.COLOUR_BLACK,
              speed=1,
              start_frame=30,
              stop_frame=50),
        Print(screen,
              FigletText("on", "banner3"),
              (screen.height - 4) // 2,
              colour=Screen.COLOUR_BLACK,
              speed=1,
              start_frame=50,
              stop_frame=70),
        Print(screen,
              FigletText("Fire!", "banner3"),
              (screen.height - 4) // 2,
              colour=Screen.COLOUR_BLACK,
              speed=1,
              start_frame=70),
    ]
    scenes.append(Scene(effects, 100))

    text = Figlet(font="banner", width=200).renderText("ASCIIMATICS")
    width = max([len(x) for x in text.split("\n")])

    effects = [
        Print(screen,
              Fire(screen.height, 80, text, 0.4, 40, screen.colours),
              0,
              speed=1,
              transparent=False),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
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
    
if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
        
# TAP-DEMO, interactive pages
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/tab_demo.py
from asciimatics.widgets import Frame, Layout, Divider, Button
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys


class TabButtons(Layout):
    def __init__(self, frame, active_tab_idx):
        cols = [1, 1, 1, 1, 1]
        super().__init__(cols)
        self._frame = frame
        for i,_ in enumerate(cols):
            self.add_widget(Divider(), i)
        btns = [Button("Btn1", self._on_click_1),
                Button("Btn2", self._on_click_2),
                Button("Btn3", self._on_click_3),
                Button("Btn4", self._on_click_4),
                Button("Quit", self._on_click_Q)]
        for i, btn in enumerate(btns):
            self.add_widget(btn, i)
        btns[active_tab_idx].disabled = True

    def _on_click_1(self):
        raise NextScene("Tab1")

    def _on_click_2(self):
        raise NextScene("Tab2")

    def _on_click_3(self):
        raise NextScene("Tab3")

    def _on_click_4(self):
        raise NextScene("Tab4")

    def _on_click_Q(self):
        raise StopApplication("Quit")


class RootPage(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         can_scroll=False,
                         title="Root Page")
        layout1 = Layout([1], fill_frame=True)
        self.add_layout(layout1)
        # add your widgets here

        layout2 = TabButtons(self, 0)
        self.add_layout(layout2)
        self.fix()


class AlphaPage(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         can_scroll=False,
                         title="Alpha Page")
        layout1 = Layout([1], fill_frame=True)
        self.add_layout(layout1)
        # add your widgets here

        layout2 = TabButtons(self, 1)
        self.add_layout(layout2)
        self.fix()


class BravoPage(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         can_scroll=False,
                         title="Bravo Page")
        layout1 = Layout([1], fill_frame=True)
        self.add_layout(layout1)
        # add your widgets here

        layout2 = TabButtons(self, 2)
        self.add_layout(layout2)
        self.fix()


class CharliePage(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         can_scroll=False,
                         title="Charlie Page")
        layout1 = Layout([1], fill_frame=True)
        self.add_layout(layout1)
        # add your widgets here

        layout2 = TabButtons(self, 3)
        self.add_layout(layout2)
        self.fix()


def demo(screen, scene):
    scenes = [
        Scene([RootPage(screen)], -1, name="Tab1"),
        Scene([AlphaPage(screen)], -1, name="Tab2"),
        Scene([BravoPage(screen)], -1, name="Tab3"),
        Scene([CharliePage(screen)], -1, name="Tab4"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
def run(last_scene=None):
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
            
            
'''
        
# RAY-CASTING, pretty impressive 3d env
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/ray_casting.py
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
from math import sin, cos, pi, copysign, floor
from asciimatics.effects import Effect
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.renderers import ColourImageFile
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import PopUpDialog


HELP = """
Use the following keys:
- Cursor keys to move.
- M to toggle the mini-map
- X to quit
- 1 to 4 to change rendering mode.
Can you find grumpy cat?
"""
LEVEL_MAP = """
XXXXXXXXXXXXXXXX
X              X
X  X        X  X
X  X  X     X  X
X XXX X  XXXX  X
X XXX X XX    XX
X X XXX    XXXXX
X X XXX XXXXX  X
X X     X      X
X XXXXX   XXXXXX
X              X
XXXXXXXXXXXXXX X
""".strip().split("\n")
IMAGE_HEIGHT = 64


class Image(object):
    """
    Class to handle image stripe rendering.
    """

    def __init__(self, image):
        self._image = image

    def next_frame(self):
        self._frame = self._image.rendered_text

    def draw_stripe(self, screen, height, x, image_x):
        # Clip required dimensions.
        y_start, y_end = 0, height
        if height > screen.height:
            y_start = (height - screen.height) // 2
            y_end = y_start + screen.height + 1

        # Draw the stripe for the required region.
        for sy in range(y_start, y_end):
            try:
                y = int((screen.height - height) / 2) + sy
                image_y = int(sy * IMAGE_HEIGHT / height)
                char = self._frame[0][image_y][image_x]
                # Unicode images use . for background only pixels; ascii ones use space.
                if char not in (" ", "."):
                    fg, attr, bg = self._frame[1][image_y][image_x]
                    attr = 0 if attr is None else attr
                    bg = 0 if bg is None else bg
                    screen.print_at(char, x, y, fg, attr, bg)
            except IndexError:
                pass


class Sprite(object):
    """
    Dynamically sized sprite.
    """

    def __init__(self, state, x, y, images):
        self._state = state
        self.x, self.y = x, y
        self._images = images

    def next_frame(self):
        for image in self._images:
            image.next_frame()

    def draw_stripe(self, height, x, image_x):
        # Resize offset in image for the expected height of this stripe.
        self._images[self._state.mode % 2].draw_stripe(
            self._state.screen, height, x, int(image_x * IMAGE_HEIGHT / height))


class GameState(object):
    """
    Persistent state for this application.
    """

    def __init__(self):
        self.player_angle = pi / 2
        self.x, self.y = 1.5, 1.5
        self.map = LEVEL_MAP
        self.mode = 0
        self.show_mini_map = True
        self.images = {}
        self.sprites = []
        self.screen = None

    def load_image(self, screen, filename):
        self.images[filename] = [None, None]
        self.images[filename][0] = Image(ColourImageFile(screen, filename, IMAGE_HEIGHT, uni=False))
        self.images[filename][1] = Image(ColourImageFile(screen, filename, IMAGE_HEIGHT, uni=True))

    def update_screen(self, screen):
        # Save off active screen.
        self.screen = screen

        # Images only need initializing once - they don't actually use the screen after construction.
        if len(self.images) <= 0:
            self.load_image(screen, "twit/free/img/grumpy_cat.jpg")
            self.load_image(screen, "twit/free/img/colour_globe.gif")
            self.load_image(screen, "twit/free/img/wall.png")

        # Demo uses static sprites, so can reset every time now we have images loaded.
        self.sprites = [
            Sprite(self, 3.5, 6.5, self.images["twit/free/img/grumpy_cat.jpg"]),
            Sprite(self, 14.5, 11.5, self.images["twit/free/img/colour_globe.gif"]),
            Sprite(self, 0, 0, self.images["twit/free/img/wall.png"])
        ]

    @property
    def map_x(self):
        return int(floor(self.x))

    @property
    def map_y(self):
        return int(floor(self.y))

    def safe_update_x(self, new_x):
        new_x += self.x
        if 0 <= self.y < len(self.map) and 0 <= new_x < len(self.map[0]):
            if self.map[self.map_y][int(floor(new_x))] == "X":
                return
        self.x = new_x

    def safe_update_y(self, new_y):
        new_y += self.y
        if 0 <= new_y < len(self.map) and 0 <= self.x < len(self.map[0]):
            if self.map[int(floor(new_y))][self.map_x] == "X":
                return
        self.y = new_y

    def safe_update_angle(self, new_angle):
        self.player_angle += new_angle
        if self.player_angle < 0:
            self.player_angle += 2 * pi
        if self.player_angle > 2 * pi:
            self.player_angle -= 2 * pi


class MiniMap(Effect):
    """
    Class to draw a small map based on the one stored in the GameState.
    """

    # Translation from angle to map directions.
    _DIRECTIONS = [
        (0, pi / 4, ">>"),
        (pi / 4, 3 * pi / 4, "vv"),
        (3 * pi / 4, 5 * pi / 4, "<<"),
        (5 * pi / 4, 7 * pi / 4, "^^")
    ]

    def __init__(self, screen, game_state, size=5):
        super(MiniMap, self).__init__(screen)
        self._state = game_state
        self._size = size
        self._x = self._screen.width - 2 * (self._size + 1)
        self._y = self._screen.height - (self._size + 1)

    def _update(self, _):
        # Draw the miniature map.
        for mx in range(self._size):
            for my in range(self._size):
                px = self._state.map_x + mx - self._size // 2
                py = self._state.map_y + my - self._size // 2
                if (0 <= py < len(self._state.map) and
                        0 <= px < len(self._state.map[0]) and self._state.map[py][px] != " "):
                    colour = Screen.COLOUR_RED
                else:
                    colour = Screen.COLOUR_BLACK
                self._screen.print_at("  ", self._x + 2 * mx, self._y + my, colour, bg=colour)

        # Draw the player
        text = ">>"
        for a, b, direction in self._DIRECTIONS:
            if a < self._state.player_angle <= b:
                text = direction
                break
        self._screen.print_at(
            text, self._x + self._size // 2 * 2, self._y + self._size // 2, Screen.COLOUR_GREEN)

    @property
    def frame_update_count(self):
        # No animation required.
        return 0

    @property
    def stop_frame(self):
        # No specific end point for this Effect.  Carry on running forever.
        return 0

    def reset(self):
        # Nothing special to do.  Just need this to satisfy the ABC.
        pass


class RayCaster(Effect):
    """
    Raycaster effect - will draw a 3D rendition of the map stored in the GameState.
    This class follows the logic from https://lodev.org/cgtutor/raycasting.html.
    """

    # Textures to emulate h distance.
    _TEXTURES = "@&#$AHhwai;:. "

    def __init__(self, screen, game_state):
        super(RayCaster, self).__init__(screen)
        # Controls for rendering.
        #
        # Ideally we'd just use a field of vision (FOV) to represent the screen aspect ratio.  However, this
        # looks wrong for very wide screens.  So, limit to 4:1 aspect ratio, then calculate FOV.
        self.width = min(screen.height * 4, screen.width)
        self.FOV = self.width / screen.height / 4

        # Remember game state for later.
        self._state = game_state

        # Set up raycasting sizes and colours
        self._block_size = screen.height // 3
        if screen.colours >= 256:
            self._colours = [x for x in zip(range(255, 232, -1), [0] * 24, range(255, 232, -1))]
        else:
            self._colours = [(Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_WHITE) for _ in range(6)]
            self._colours.extend([(Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_WHITE) for _ in range(9)])
            self._colours.extend([(Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK) for _ in range(9)])
            self._colours.append((Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK))

    def _update(self, _):
        # First draw the background - which is theoretically the floor and ceiling.
        self._screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)

        # Now do the ray casting across the visible canvas.
        # Compensate for aspect ratio by treating 2 cells as a single pixel.
        x_offset = int((self._screen.width - self.width ) // 2)
        last_side = None
        z_buffer = [999999 for _ in range(self.width + 1)]
        camera_x = cos(self._state.player_angle + pi / 2) * self.FOV
        camera_y = sin(self._state.player_angle + pi / 2) * self.FOV
        for sx in range(0, self.width, 2 - self._state.mode // 2):
            # Calculate the ray for this vertical slice.
            camera_segment = 2 * sx / self.width - 1
            ray_x = cos(self._state.player_angle) + camera_x * camera_segment
            ray_y = sin(self._state.player_angle) + camera_y * camera_segment

            # Representation of the ray within our map
            map_x = self._state.map_x
            map_y = self._state.map_y
            hit = False
            hit_side = False

            # Logical length along the ray from one x or y-side to next x or y-side
            try:
                ratio_to_x = abs(1 / ray_x)
            except ZeroDivisionError:
                ratio_to_x = 999999
            try:
                ratio_to_y = abs(1 / ray_y)
            except ZeroDivisionError:
                ratio_to_y = 999999

            # Calculate block step direction and initial partial step to the next side (on same
            # logical scale as the previous ratios).
            step_x = int(copysign(1, ray_x))
            step_y = int(copysign(1, ray_y))
            side_x = (self._state.x - map_x) if ray_x < 0 else (map_x + 1.0 - self._state.x)
            side_x *= ratio_to_x
            side_y = (self._state.y - map_y) if ray_y < 0 else (map_y + 1.0 - self._state.y)
            side_y *= ratio_to_y

            # Give up if we'll never intersect the map
            while (((step_x < 0 and map_x >= 0) or (step_x > 0 and map_x < len(self._state.map[0]))) and
                   ((step_y < 0 and map_y >= 0) or (step_y > 0 and map_y < len(self._state.map)))):
                # Move along the ray to the next nearest side (measured in distance along the ray).
                if side_x < side_y:
                    side_x += ratio_to_x
                    map_x += step_x
                    hit_side = False
                else:
                    side_y += ratio_to_y
                    map_y += step_y
                    hit_side = True

                # Check whether the ray has now hit a wall.
                if 0 <= map_x < len(self._state.map[0]) and 0 <= map_y < len(self._state.map):
                    if self._state.map[map_y][map_x] == "X":
                        hit = True
                        break

            # Draw wall if needed.
            if hit:
                # Figure out textures and colours to use based on the distance to the wall.
                if hit_side:
                    dist = (map_y - self._state.y + (1 - step_y) / 2) / ray_y
                else:
                    dist = (map_x - self._state.x + (1 - step_x) / 2) / ray_x
                z_buffer[sx], z_buffer[sx + 1] = dist, dist

                # Are we drawing block colours or ray traced walls?
                if self._state.mode < 2:
                    # Simple block colours - get height and text attributes
                    wall = min(self._screen.height, int(self._screen.height / dist))
                    colour, attr, bg = self._colours[min(len(self._colours) - 1, int(3 * dist))]
                    text = self._TEXTURES[min(len(self._TEXTURES) - 1, int(2 * dist))]

                    # Now draw the wall segment
                    for sy in range(wall):
                        self._screen.print_at(
                            text * 2, x_offset + sx, (self._screen.height - wall) // 2 + sy,
                            colour, attr, bg=0 if self._state.mode == 0 else bg)
                else:
                    # Ray casting - get wall texture
                    image = self._state.images["wall.png"][self._state.mode % 2]

                    # Get texture height and stripe offset bearing in mind pixels are 1x2 aspect ratio.
                    wall = int(self._screen.height / dist)
                    if hit_side:
                        wall_x = self._state.x + dist * ray_x;
                    else:
                        wall_x = self._state.y + dist * ray_y;
                    wall_x -= int(wall_x);
                    texture_x = int(wall_x * IMAGE_HEIGHT * 2);
                    if (not hit_side) and ray_x > 0:
                        texture_x = IMAGE_HEIGHT * 2 - texture_x - 1;
                    if hit_side and ray_y < 0:
                        texture_x = IMAGE_HEIGHT * 2 - texture_x - 1;

                    # Now draw it
                    image.next_frame()
                    image.draw_stripe(self._screen, wall, x_offset + sx, texture_x)

                # Draw a line when we change surfaces to help make it easier to see the 3d effect
                if hit_side != last_side:
                    last_side = hit_side
                    for sy in range(wall):
                        self._screen.print_at("|", x_offset + sx, (self._screen.height - wall) // 2 + sy, 0, bg=0)

        # Now draw sprites
        ray_x = cos(self._state.player_angle)
        ray_y = sin(self._state.player_angle)
        for sprite in self._state.sprites:
            # Translate sprite position to relative to camera
            sprite_x = sprite.x - self._state.x
            sprite_y = sprite.y - self._state.y
            inv_det = 1.0 / (camera_x * ray_y - ray_x * camera_y)
            transform_x = inv_det * (ray_y * sprite_x - ray_x * sprite_y);
            transform_y = inv_det * (-camera_y * sprite_x + camera_x * sprite_y)

            # Sprite location on camera plane.
            sprite_screen_x = int((self.width / 2) * (1 + transform_x / transform_y));

            # Calculate height (and width) of the sprite on screen
            sprite_height = abs(int(self._screen.height / (transform_y)))

            # Don't bother if behind the viewing plane (or too big to render).
            if transform_y > 0:
                # Update for animation
                sprite.next_frame()

                # Loop through every vertical stripe of the sprite on screen
                start = max(0, sprite_screen_x - sprite_height)
                end = min(self.width, sprite_screen_x + sprite_height)
                for stripe in range(start, end):
                    if stripe > 0 and stripe < self.width and transform_y < z_buffer[stripe]:
                        texture_x = int(stripe - (-sprite_height + sprite_screen_x) * sprite_height / sprite_height)
                        sprite.draw_stripe(sprite_height, x_offset + stripe, texture_x)

    @property
    def frame_update_count(self):
        # Animation required - every other frame should be OK for demo.
        return 2

    @property
    def stop_frame(self):
        # No specific end point for this Effect.  Carry on running forever.
        return 0

    def reset(self):
        # Nothing special to do.  Just need this to satisfy the ABC.
        pass


class GameController(Scene):
    """
    Scene to control the combined Effects for the demo.
    This class handles the user input, updating the game state and updating required Effects as needed.
    Drawing of the Scene is then handled in the usual way.
    """

    def __init__(self, screen, game_state):
        # Standard setup for every screen.
        self._screen = screen
        self._state = game_state
        self._mini_map = MiniMap(screen, self._state, self._screen.height // 4)
        effects = [
            RayCaster(screen, self._state)
        ]
        super(GameController, self).__init__(effects, -1)

        # Add minimap if required.
        if self._state.show_mini_map:
            self.add_effect(self._mini_map)

    def process_event(self, event):
        # Allow standard event processing first
        if super(GameController, self).process_event(event) is None:
            return

        # If that didn't handle it, check for a key that this demo understands.
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c in (ord("x"), ord("X")):
                raise StopApplication("User exit")
            elif c in (ord("a"), Screen.KEY_LEFT):
                self._state.safe_update_angle(-pi / 45)
            elif c in (ord("d"), Screen.KEY_RIGHT):
                self._state.safe_update_angle(pi / 45)
            elif c in (ord("w"), Screen.KEY_UP):
                self._state.safe_update_x(cos(self._state.player_angle) / 5)
                self._state.safe_update_y(sin(self._state.player_angle) / 5)
            elif c in (ord("s"), Screen.KEY_DOWN):
                self._state.safe_update_x(-cos(self._state.player_angle) / 5)
                self._state.safe_update_y(-sin(self._state.player_angle) / 5)
            elif c in (ord("1"), ord("2"), ord("3"), ord("4")):
                self._state.mode = c - ord("1")
            elif c in (ord("m"), ord("M")):
                self._state.show_mini_map = not self._state.show_mini_map
                if self._state.show_mini_map:
                    self.add_effect(self._mini_map)
                else:
                    self.remove_effect(self._mini_map)
            elif c in (ord("h"), ord("H")):
                self.add_effect(PopUpDialog(self._screen, HELP, ["OK"]))
            else:
                # Not a recognised key - pass on to other handlers.
                return event
        else:
            # Ignore other types of events.
            return event


def demo(screen, game_state):
    game_state.update_screen(screen)
    screen.play([GameController(screen, game_state)], stop_on_resize=True)


def run():
    game_state = GameState()
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[game_state])
            sys.exit(0)
        except ResizeScreenError:
            pass
'''        
# PLASMA - COOL but hardcore lags the computer
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/plasma.py
from random import choice
from asciimatics.renderers import Plasma, Rainbow, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
import sys


class PlasmaScene(Scene):
    
    # Random cheesy comments
    _comments = [''
        #"Far out!",
        #"Groovy",
        #"Heavy",
        #"Right on!",
        #"Cool",
        #"Dude!"
    ]
    
    def __init__(self, screen):
        self._screen = screen
        effects = [
            Print(screen,
                  Plasma(screen.height, screen.width, screen.colours),
                  0,
                  speed=1,
                  transparent=False),
        ]
        super(PlasmaScene, self).__init__(effects, 200, clear=False)

    def _add_cheesy_comment(self):
        msg = FigletText(choice(self._comments), "banner3")
        self._effects.append(
            Print(self._screen,
                  msg,
                  (self._screen.height // 2) - 4,
                  x=(self._screen.width - msg.max_width) // 2 + 1,
                  colour=Screen.COLOUR_BLACK,
                  stop_frame=80,
                  speed=1))
        self._effects.append(
            Print(self._screen,
                  Rainbow(self._screen, msg),
                  (self._screen.height // 2) - 4,
                  x=(self._screen.width - msg.max_width) // 2,
                  colour=Screen.COLOUR_BLACK,
                  stop_frame=80,
                  speed=1))

    def reset(self, old_scene=None, screen=None):
        super(PlasmaScene, self).reset(old_scene, screen)

        # Make sure that we only have the initial Effect and add a new cheesy
        # comment.
        self._effects = [self._effects[0]]
        self._add_cheesy_comment()


def demo(screen):
    screen.play([PlasmaScene(screen)], stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
'''

# JULIA FRACTAL
''' https://github.com/peterbrittain/asciimatics/blob/master/samples/julia.py
from asciimatics.effects import Julia
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    scenes = []
    effects = [
        Julia(screen),
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
        
# INTERACTIVE
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/interactive.py
from asciimatics.effects import Sprite, Print
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import StaticRenderer, SpeechBubble, FigletText
from asciimatics.screen import Screen
from asciimatics.paths import DynamicPath
from asciimatics.sprites import Arrow
from asciimatics.scene import Scene
import sys

# Sprites used for the demo
arrow = None
cross_hairs = None


class KeyboardController(DynamicPath):
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_UP:
                self._y -= 1
                self._y = max(self._y, 2)
            elif key == Screen.KEY_DOWN:
                self._y += 1
                self._y = min(self._y, self._screen.height-2)
            elif key == Screen.KEY_LEFT:
                self._x -= 1
                self._x = max(self._x, 3)
            elif key == Screen.KEY_RIGHT:
                self._x += 1
                self._x = min(self._x, self._screen.width-3)
            else:
                return event
        else:
            return event


class MouseController(DynamicPath):
    def __init__(self, sprite, scene, x, y):
        super(MouseController, self).__init__(scene, x, y)
        self._sprite = sprite

    def process_event(self, event):
        if isinstance(event, MouseEvent):
            self._x = event.x
            self._y = event.y
            if event.buttons & MouseEvent.DOUBLE_CLICK != 0:
                # Try to whack the other sprites when mouse is clicked
                self._sprite.whack("KERPOW!")
            elif event.buttons & MouseEvent.LEFT_CLICK != 0:
                # Try to whack the other sprites when mouse is clicked
                self._sprite.whack("BANG!")
            elif event.buttons & MouseEvent.RIGHT_CLICK != 0:
                # Try to whack the other sprites when mouse is clicked
                self._sprite.whack("CRASH!")
        else:
            return event


class TrackingPath(DynamicPath):
    def __init__(self, scene, path):
        super(TrackingPath, self).__init__(scene, 0, 0)
        self._path = path

    def process_event(self, event):
        return event

    def next_pos(self):
        x, y = self._path.next_pos()
        return x + 8, y - 2


class Speak(Sprite):
    def __init__(self, screen, scene, path, text, **kwargs):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(Speak, self).__init__(
            screen,
            renderer_dict={
                "default": SpeechBubble(text, "L")
            },
            path=TrackingPath(scene, path),
            colour=Screen.COLOUR_CYAN,
            **kwargs)


class InteractiveArrow(Arrow):
    def __init__(self, screen):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(InteractiveArrow, self).__init__(
            screen,
            path=KeyboardController(
                screen, screen.width // 2, screen.height // 2),
            colour=Screen.COLOUR_GREEN)

    def say(self, text):
        self._scene.add_effect(
            Speak(self._screen, self._scene, self._path, text, delete_count=50))


class CrossHairs(Sprite):
    def __init__(self, screen):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(CrossHairs, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=["X"])
            },
            path=MouseController(
                self, screen, screen.width // 2, screen.height // 2),
            colour=Screen.COLOUR_RED)

    def whack(self, sound):
        x, y = self._path.next_pos()
        if self.overlaps(arrow, use_new_pos=True):
            arrow.say("OUCH!")
        else:
            self._scene.add_effect(Print(
                self._screen,
                SpeechBubble(sound), y, x, clear=True, delete_count=50))


def demo(screen):
    global arrow, cross_hairs
    arrow = InteractiveArrow(screen)
    cross_hairs = CrossHairs(screen)

    scenes = []
    effects = [
        Print(screen, FigletText("Hit the arrow with the mouse!", "digital"),
              y=screen.height//3-3),
        Print(screen, FigletText("Press space when you're ready.", "digital"),
              y=2 * screen.height//3-3),
    ]
    scenes.append(Scene(effects, -1))

    effects = [
        arrow,
        cross_hairs
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
# ASCII IMAGE RENDERING
'''https://github.com/peterbrittain/asciimatics/blob/master/samples/images.py
from __future__ import division
from asciimatics.effects import BannerText, Print, Scroll
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys


def demo(screen):
    scenes = []
    effects = [
        
        Print(screen, ImageFile("/home/brandon/twit_dev/twit/free/img/globe.gif", screen.height - 2, colours=screen.colours),
              0,
              stop_frame=100),
    ]
    scenes.append(Scene(effects))
    effects = [
        Print(screen,
              ColourImageFile(screen, "/home/brandon/twit_dev/twit/free/img/colour_globe.gif", screen.height-2,
                              uni=screen.unicode_aware,
                              dither=screen.unicode_aware),
              0,
              stop_frame=200),
        Print(screen,
              FigletText("ASCIIMATICS",
                         font='banner3' if screen.width > 80 else 'banner'),
              screen.height//2-3,
              colour=7, bg=7 if screen.unicode_aware else 0),
    ]
    scenes.append(Scene(effects))
    effects = [
        Print(screen,
              ColourImageFile(screen, "/home/brandon/twit_dev/twit/free/img/grumpy_cat.jpg", screen.height,
                              uni=screen.unicode_aware),
              screen.height,
              speed=1,
              stop_frame=(40+screen.height)*3),
        Scroll(screen, 3)
    ]
    scenes.append(Scene(effects))
    effects = [
        BannerText(screen,
                   ColourImageFile(screen, "/home/brandon/twit_dev/twit/free/img/python.png", screen.height-2,
                                   uni=screen.unicode_aware, dither=screen.unicode_aware),
                   0, 0),
    ]
    scenes.append(Scene(effects))

    screen.play(scenes, stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass        

'''

'''https://github.com/peterbrittain/asciimatics/blob/master/samples/credits.py
from __future__ import division
import sys
from pyfiglet import Figlet

from asciimatics.effects import Scroll, Mirage, Wipe, Cycle, Matrix, \
    BannerText, Stars, Print
from asciimatics.particles import DropScreen
from asciimatics.renderers import FigletText, SpeechBubble, Rainbow, Fire
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError


def _credits(screen):
    scenes = []

    text = Figlet(font="banner", width=200).renderText("ASCIIMATICS")
    width = max([len(x) for x in text.split("\n")])

    effects = [
        Print(screen,
              Fire(screen.height, 80, text, 0.4, 40, screen.colours),
              0,
              speed=1,
              transparent=False),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
    ]
    scenes.append(Scene(effects, 100))

    effects = [
        Matrix(screen, stop_frame=200),
        Mirage(
            screen,
            FigletText("Asciimatics"),
            screen.height // 2 - 3,
            Screen.COLOUR_GREEN,
            start_frame=100,
            stop_frame=200),
        Wipe(screen, start_frame=150),
        Cycle(
            screen,
            FigletText("Asciimatics"),
            screen.height // 2 - 3,
            start_frame=200)
    ]
    scenes.append(Scene(effects, 250, clear=False))

    effects = [
        BannerText(
            screen,
            Rainbow(screen, FigletText(
                "Reliving the 80s in glorious ASCII text...", font='slant')),
            screen.height // 2 - 3,
            Screen.COLOUR_GREEN)
    ]
    scenes.append(Scene(effects))

    effects = [
        Scroll(screen, 3),
        Mirage(
            screen,
            FigletText("Conceived and"),
            screen.height,
            Screen.COLOUR_GREEN),
        Mirage(
            screen,
            FigletText("written by:"),
            screen.height + 8,
            Screen.COLOUR_GREEN),
        Mirage(
            screen,
            FigletText("Peter Brittain"),
            screen.height + 16,
            Screen.COLOUR_GREEN)
    ]
    scenes.append(Scene(effects, (screen.height + 24) * 3))

    colours = [Screen.COLOUR_RED, Screen.COLOUR_GREEN,]
    contributors = [
        "Cory Benfield",
        "Bryce Guinta",
        "Aman Orazaev",
        "Daniel Kerr",
        "Dylan Janeke",
        "ianadeem",
        "Scott Mudge",
        "Luke Murphy",
        "mronkain",
        "Dougal Sutherland",
        "Kirtan Sakariya",
        "Jesse Lieberg",
        "Erik Doffagne",
        "Noah Ginsburg",
        "Davidy22",
        "Christopher Trudeau",
        "Beniamin Kalinowski"
    ]

    effects = [
        Scroll(screen, 3),
        Mirage(
            screen,
            FigletText("With help from:"),
            screen.height,
            Screen.COLOUR_GREEN,
        )
    ]

    pos = 8
    for i, name in enumerate(contributors):
        effects.append(
            Mirage(
                screen,
                FigletText(name),
                screen.height + pos,
                colours[i % len(colours)],
            )
        )

        pos += 8
    scenes.append(Scene(effects, (screen.height + pos) * 3))

    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 8,
            stop_frame=100),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3,
            stop_frame=100),
        Stars(screen, (screen.width + screen.height) // 2, stop_frame=100),
        DropScreen(screen, 200, start_frame=100)
    ]
    scenes.append(Scene(effects, 300))

    effects = [
        Print(screen,
              SpeechBubble("Press 'X' to exit."), screen.height // 2 - 1, attr=Screen.A_BOLD)
    ]
    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True)


def run():
    while True:
        try:
            Screen.wrapper(_credits)
            sys.exit(0)
        except ResizeScreenError:
            pass
        
'''