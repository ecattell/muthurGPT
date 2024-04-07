from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

VEHICLE_DOOR_MESSAGE = """\"VEHICLE BAY DECOMPRESSION RECOMMENDED
BEFORE OPENING VEHICLE BAY DOOR.
EVACUATE ALL PERSONNEL FROM VEHICLE BAY.

CONFIRM FROM FOLLOWING OPTIONS:
1) RECOMMENDED: PROCEED WITH 7 MINUTE DECOMPRESSION PROCESS BEFORE DOOR OPEN.
2) BYPASS DECOMPRESSION PROCESS TO OPEN DOOR IMMEDIATELY.\"

If they choose option 2, warn them before proceeding. This will depressurize most of Decks C and D.

No confirmation is needed to close the door again. Repressurization will be automatic."""

@register_plugin
class CronusPlugin(Plugin):
    """
    Plugin to represent the Cronus in the Chariot of the Gods cinematic.
    """
    NAME = "cronus"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            CronusPlugin.NAME, config, terminal, path_resolver)

        with open(self.path_resolver.get_ascii_path("WEYLAND_LOGO"), "r") as f:
            self.logo = f.read()

        with open(self.path_resolver.get_ascii_path("BOOT_TEXT"), "r") as f:
            self.boot_text = f.read()

    def filter_bot_reply(self, bot_reply):
        if "COMMAND SEQUENCE OVERRIDE" in bot_reply:
            self.react_command_sequence_override()
        return bot_reply

    def filter_plugin_prompt(self, prompt):
        #TODO This could be made cleaner. Maybe specify these as pairs in config, and enable them via --update arg?

        if self.config.get("garage_locked"):
            prompt += "\nThe garage door of the vehicle bay is currently locked. A crew member will need to physically remove the lock from the door before it can be opened."
        else:
            prompt += f"\nThe garage door in the Vehicle Garage of Deck D is functional. If users attempt to open it, write the following and give them these options:\n{VEHICLE_DOOR_MESSAGE}"
        if self.config.get("cronus_cryo_ended"):
            prompt += "\n UPDATE: At this point, the players have already woken the crew from cryo. You no longer know their status or where they are."
        if self.config.get("cronus_main_airlock_open"):
            prompt += "\n UPDATE: At this point, the players have opened the main airlock on Deck A from the outside and are docked to it."
        if self.config.get("cronus_main_airlock_broken"):
            prompt += "\n UPDATE: The main airlock on Deck A is damaged."
        if self.config.get("cronus_life_support_restored"):
            prompt += "\n UPDATE: At this point, life support is already fully powered on. Low power mode is off, and temperature has returned to normal."
        if self.config.get("cronus_oxygen_restored"):
            prompt += "\n UPDATE: At this point, the crew have already restored oxygen."
        if self.config.get("main_airlock_broken"):
            prompt += "\n UPDATE: At this point, the main airlock on Deck A is unable to pressurize. Direct users to inspect for damage."
        if self.config.get("garage_open"):
            prompt += "\n UPDATE: At this point, the vehicle bay garage door is open and the vehicle bay is depressurized. A user could close the door through you and repressurize the vehicle bay."
        if self.config.get("return_to_earth"):
            prompt += "\n UPDATE: The Cronus is returning to Earth due to Special Order 966. The order is classifed. The order is immutable, and can not be cancelled. The course can not be redirected."
        if self.config.get("engine_repaired"):
            prompt += "\n UPDATE: The engine has now been repaired by the crew."
        if self.config.get("nav_repaired"):
            prompt += "\n UPDATE: The nav system has now been repaired by the crew."
        if self.config.get("comm_repaired"):
            prompt += "\n UPDATE: The communication system has now been repaired by the crew."
        if self.config.get("reactor_repaired"):
            prompt += "\n UPDATE: The reactor has now been repaired by the crew."
        if self.config.get("scrubbers_repaired"):
            prompt += "\n UPDATE: The scrubbers have now been repaired by the crew."
        if self.config.get("reveal_eev"):
            prompt += "\n UPDATE: There is one EEV (Emergency Escape Vehicle) on the ship that has recently been powered on. 1) It is in the Corporate Suite on Deck B. 2) It contains three cryobeds and no FTL capabilities. 3) You became aware of its existence when the boot process was initiated by Clayton. You don't know how long that boot process takes."
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
            return "Enabling life support."
        return ""