import os
import random
import subprocess
import re
import time
from termcolor import colored

from muthur_gpt import constants

class MuthurTerminal():
    """
    This module handles the display and sound of the MU/TH/UR terminal.
    """
    def __init__(self, config, path_resolver, mute):
        self.config = config
        self.path_resolver = path_resolver
        self.mute = mute

    def clear(self):
        os.system("clear")

    def print_header(self):
        muthur_name = self.config.get(constants.CONFIG_KEY_HEADER_NAME)
        header = " "*constants.TITLE_OFFSET_LEN + F"╠█▓▒░  {muthur_name}  "
        self.print_instant(header + "░"*(self.width-len(header)))
        self.print_hbar()

    def print_hbar(self, character="▀"):
        self.print_instant(character * self.width)

    def print_space(self, count):
        for i in range(count):
            # TODO add tick sound here?
            time.sleep(.01)  #TODO add this to config?
            print("")

    def print_random_line(self, char_choices, color_choices):
        """
        Draw one line of random chars, given the selection of chars/colors
        """
        for i in range(0, self.width):
            char = random.choice(char_choices)
            color = random.choice(color_choices)
            print(colored(char,color), end="", flush=True)

    def print_noise_screen(self, display_time, line_draw_time=0.01,
            char_choices=["█", "▓", "▒", "░"],
            color_choices=["green","light_green","light_cyan"]):
        """
        Fill the screen with random ascii noise
        """
        for line in range(self.height):
            time.sleep(line_draw_time)
            self.print_random_line(char_choices, color_choices)
        time.sleep(display_time)

    def print_progress_bar(
            self, prependText, draw_time=1, character="▒",
            l_margin=0, r_margin=4):
        """
        Draw a progress bar on screen.
        """
        print(" " * l_margin, prependText, end="", flush=True)
        bar_char_count = max(self.width - l_margin - len(prependText) - r_margin, 1)
        time_per_char = draw_time / bar_char_count
        for i in range(0, bar_char_count):
            print(character, end="", flush=True)
            time.sleep(time_per_char)
        self.print_space(1)

    def print_instant(self, text):
        """
        Wrapper around print, in case we add sound / etc or separate
        application stdout logging from in-universe terminal
        """
        print(text)

    def print_slow(self, text, speed=None, sound=True):
        if not speed:
            speed = self.config.get(constants.CONFIG_KEY_DEFAULT_SPEED)
        process = self.play_sound("typing_long")
        for char in text:
            print(char, end="", flush=True)
            time.sleep(speed)
            if sound and not self.mute:
                poll = process.poll()
                if poll is not None:
                    # Sound is over
                    process = self.play_sound("subtle_long_type")
                elif char == "\n":
                    return_sound_name = "loud_type_start"
                    process = self.play_sound(return_sound_name)
        self.print_space(1)
        if process:
            process.kill()

    def print_reply(self, text):
        """
        Process a reply, substituting tags for ascii_art
        """
        # Split the text into segments of regular text and image tags
        segments = re.split(r"(<IMG:[^>]+>)", text)
        for segment in segments:
            # Skip extra whitespace between segments
            if not segment: continue
            # Check if the segment is an image tag
            match = re.match(r"<IMG:(.*?)>", segment)
            if match:
                image_name = match.group(1)
                self.display_image(image_name)
            else:
                if self.config.get(constants.CONFIG_KEY_FORCE_UPPER_CASE):
                    segment = segment.upper()
                if self.config.get(constants.CONFIG_KEY_TEXT_TO_SPEECH):
                    self.say(segment)
                    self.print_slow_lines(segment)
                else:
                    self.print_slow(segment)

    def say(self, text):
        """
        This was an experiment, but keeping it here for potential expansion
        """
        from gtts import gTTS
        from playsound import playsound
        import tempfile
        filename = os.path.join(tempfile.gettempdir(), 'voice.mp3')
        tts = gTTS(text)
        tts.save(filename)
        subprocess.Popen(["afplay", filename])

    def print_slow_lines(self, text, speed=None, sound=True):
        if not speed:
            speed = self.config.get(constants.CONFIG_KEY_DEFAULT_SPEED)
        process = self.play_sound("typing_long")
        for line in text.split("\n"):
            print(line)
            time.sleep(speed)
            if sound and not self.mute:
                poll = process.poll()
                if poll is not None:
                    # Sound is over
                    process = self.play_sound("subtle_long_type")
        self.print_space(1)
        if process:
            process.kill()

    def print_previous_input(self, user_input):
        self.print_space(constants.PREV_INPUT_TOP_MARGIN)
        if user_input:
            self.print_instant(self.input_prefix + user_input)
        else:
            print()

    def get_input(self, sound_name="beep"):
        self.wait(self.config.get(constants.CONFIG_KEY_PROMPT_WAIT_TIME))
        self.play_sound(sound_name)
        #TODO base number of newlines on terminal height and number lines
        self.print_space(6)
        return input(self.input_prefix)

    def wait(self, wait_time):
        """
        Separating in-universe terminal out in case we multithread this
        """
        time.sleep(wait_time)

    def play_sound(self, sound_name):
        if not self.mute:
            sound_path = self.path_resolver.get_sound_path(sound_name)
            if not sound_path:
                raise Exception(f"Sound file unresolved for {sound_name}")
            return subprocess.Popen(["afplay", sound_path])

    def display_image(self, image_name):
        """
        Currently printed, but would be interesting to display an image instead
        """
        self.play_sound("screen_display")

        try:
            with open(self.path_resolver.get_ascii_path(image_name), "r") as f:
                ascii_image = f.read()
        except:
            # If image isn't readable or path doesn't exist
            ascii_image = f"[IMAGE {image_name} CORRUPTED]"

        # Add margin
        ascii_image = "\n"*constants.IMAGE_TOP_MARGIN + ascii_image + \
            "\n"*constants.IMAGE_BOTTOM_MARGIN

        self.print_slow_lines(
            ascii_image,
            self.config.get(constants.CONFIG_KEY_MAP_SPEED),
            sound=True)

    @property
    def width(self):
        """ Terminal width in chars """
        return os.get_terminal_size().columns

    @property
    def height(self):
        """ Terminal height in lines """
        return os.get_terminal_size().lines

    @property
    def input_prefix(self):
        """
        Prefix before taking user input or displaying previous user input
        """
        return constants.INPUT_INDENT_LEN * " " + "»  "
