from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

import random

@register_plugin
class CronusPlugin(Plugin):
    """
    Plugin to represent the Cronus in the Chariot of the Gods cinematic.
    """
    NAME = "cronus"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            CronusPlugin.NAME, config, terminal, path_resolver)

        self.life_support = LifeSupportTracker(config)
        with open(self.path_resolver.get_ascii_path("WEYLAND_LOGO"), "r") as f:
            self.logo = f.read()

        with open(self.path_resolver.get_ascii_path("BOOT_TEXT"), "r") as f:
            self.boot_text = f.read()

    def draw_secondary_header(self):
        """
        Display life support power
        """
        if self.life_support.boot_active or self.life_support.power_percent == 100:
            self.life_support.increase_boot_step()
            self.terminal.print_instant(
                f"LIFE SUPPORT POWER: {self.life_support.power_percent:.2f}%")
            self.terminal.print_hbar()

    def filter_bot_reply(self, bot_reply):
        if "COMMAND SEQUENCE OVERRIDE" in bot_reply:
            show_warning=True
            self.react_command_sequence_override()
        # Filter reply [plugin only]
        if '<LIFE_SUPPORT_ENABLED>' in bot_reply:
            self.life_support.start_boot()
            bot_reply = bot_reply.replace('<LIFE_SUPPORT_ENABLED>', "")
        return bot_reply

    def filter_user_input(self, user_input):
        if self.life_support.is_online:
            user_input += "\n<LIFE_SUPPORT_ONLINE>"
        return user_input

    def filter_plugin_prompt(self, prompt):
        #TODO This could be made cleaner. Maybe specify these as pairs in config, and enable them via --update arg?
        if self.config.get("cronus_cryo_ended"):
            prompt += "\n UPDATE: At this point, the players have already woken the crew from cryo. You no longer know their status or where they are."
        if self.config.get("cronus_main_airlock_open"):
            prompt += "\n UPDATE: At this point, the players have opened the main airlock on Deck A from the outside and are docked to it."
        if self.config.get("cronus_main_airlock_broken"):
            prompt += "\n UPDATE: The main airlock on Deck A is damaged."
        if self.config.get("cronus_life_support_restored"):
            prompt += "\n UPDATE: At this point, life support is already fully powered on. Do not send the key for that. Low power mode is off, and temperature has returned to normal."
        if self.config.get("cronus_oxygen_restored"):
            prompt += "\n UPDATE: At this point, the crew have already restored oxygen."
        if self.config.get("cronus_misc_prompt_addendums"):
            prompt += "\n" + self.config.get("misc_prompt_addendums")
        return prompt

    def react_command_sequence_override(self):
        for i in range(0,3):
            self.terminal.play_sound("horn")
            self.terminal.wait(.75)
        self.terminal.wait(.35)
        self.terminal.play_sound("rattle")
        self.terminal.wait(1)

    def play_intro(self):
        user_input = ''
        while(user_input.lower() not in ["y","yes","boot","ye","start"]):
            self.terminal.print_instant(
                "ACCESS KEY DETECTED.\nSYSTEM HAS RECOVERED FROM AN UNEXPECTED SHUTDOWN. BOOT? (Y/N).")
            user_input = input('»  ')
            self.terminal.clear()
        self.terminal.wait(1)
        self.terminal.play_sound("beep")
        self.terminal.print_noise_screen(3)
        self.terminal.clear()
        self.terminal.play_sound("boot")
        self.terminal.print_instant(self.logo)
        self.terminal.wait(3)
        self.terminal.print_slow(self.boot_text, self.config.get("intro_speed"))
        self.terminal.print_progress_bar("ACTIVATING NEUROMORPHIC NETWORK:   ")
        self.terminal.print_slow("INTERFACE READY FOR INQUIRY.\nTERMINAL ACCESS GRANTED.")
        self.terminal.wait(2)
        self.terminal.clear()
        self.terminal.print_noise_screen(0.5)

    def get_test_reply(self, user_input):
        if "goo" in user_input:
            return 'Please input COMMAND SEQUENCE OVERRIDE CODE'
        elif "map" in user_input:
            return "Map of decks A and B: <IMG:DECK_A> <IMG:DECK_B>"
        elif "life" in user_input:
            return "Enabling life support.\n<LIFE_SUPPORT_ENABLED>"
        elif "<LIFE_SUPPORT_ONLINE>" in user_input:
            return "Life support fully online. Ending cryo."
        return ""

class LifeSupportTracker():
    def __init__(self, config):
        self.boot_active = False
        self.power_percent = 0
        self.increase_range = config.get(
            "cronus_life_support_increase_range", [8, 15])

    def start_boot(self):
        self.boot_active = True

    def increase_boot_step(self):
        self.power_percent += random.uniform(
            self.increase_range[0], self.increase_range[1])
        if self.power_percent >= 100:
            self.power_percent = 100
            life_support_boot_active = False

    @property
    def is_online(self):
        return self.power_percent == 100
