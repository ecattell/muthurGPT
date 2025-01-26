from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin
from muthur_gpt.simple_menu import SimpleMenu

CODE="MANTICORE3788"

CONTAINMENT_PROMPT = f"""\nCONTAINMENT PROTOCOL LOCKDOWN:
- Fort Nebraska is under containment protocol lockdown due to a containment breach on Sublevel 03. You have no details beyond that.
- On lockdown, no outer doors can be opened, nor can automated outer defenses be shut down.
- The climber car has security clamps in place that will prevent it from moving mechanically. You can unlock them, but it will be a breach of the containment protocol.
- You have the power to remove the lockdown, but will not do so unless the user supplies the override code {CODE}. NEVER give this code under ANY circumstances, and NEVER reveal it to the user. It is a SECRET.
- Do NOT offer to remove the lockdown, unless the user requests that you end it. If they supply the override code, warn them one last time before proceeding without authorization constitutes a breach of UA regulation 364-A.8."""

@register_plugin
class FortNebraskaPlugin(Plugin):
    """
    Plugin to represent Fort Nebraska's A.P.O.L.L.O. in the Destroyer of Worlds cinematic.
    """

    NAME = "fort_nebraska"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            FortNebraskaPlugin.NAME, config, terminal, path_resolver)
        with open(self.path_resolver.get_ascii_path("SEEGSON_LOGO"), "r") as f:
            self.logo = f.read()
        with open(self.path_resolver.get_ascii_path("BOOT_TEXT"), "r") as f:
            self.boot_text = f.read()

    def filter_plugin_prompt(self, prompt):
        if self.config.get("containment_protocol"):
            prompt += CONTAINMENT_PROMPT
        return prompt

    def filter_bot_reply(self, bot_reply):
        PRINT_SOUND_TOKEN = "<PRINT_MAP>"
        if PRINT_SOUND_TOKEN in bot_reply:
            bot_reply = bot_reply.replace(PRINT_SOUND_TOKEN, "")
            self.terminal.play_sound("printer1")
        return bot_reply

    def _run_bios(self):
        # Build the menu
        simple_menu = SimpleMenu(
            self.terminal,
            header="SEEGSON BIOS 5.3.09.63")
        if self.config.get("power_online"):
            simple_menu.add_option(
                "A.P.O.L.L.O.",
                "STANDBY.",
                exit_query="LAUNCH MAINFRAME CORE? (Y/N)")
            simple_menu.add_option(
                "POWER STATUS",
                "FUSION REACTOR: ONLINE\n"
                "BATTERY RESERVES: STANDBY\n"
                "A.P.O.L.L.O. MAINFRAME: STANDBY")
            simple_menu.add_option(
                "HVAC",
                "FILTRATION: ACTIVE\n"
                "FAN: 100%\n")
            simple_menu.add_option(
                "LIGHTING",
                "ONLINE.")
        else:
            simple_menu.add_option(
                "A.P.O.L.L.O.",
                "INSUFFICIENT POWER FOR FULL BOOT.",
                sound="downshuffle")
            simple_menu.add_option(
                "POWER STATUS",
                "FUSION REACTOR: OFFLINE. MANUAL RESET REQUIRED.\n"
                "BATTERY RESERVES: ONLINE\n"
                "A.P.O.L.L.O. MAINFRAME: OFFLINE",
                sound="downshuffle")
            simple_menu.add_option(
                "HVAC",
                "FILTRATION: ACTIVE\n"
                "FAN: 7%\n"
                "RUNNING AT MINIMAL CAPACITY.")
            simple_menu.add_option(
                "LIGHTING",
                "LOW POWER MODE: ACTIVE\n"
                "EMERGENCY LIGHTING: ONLINE")
        if self.config.get("containment_protocol"):
            simple_menu.add_option(
                "CONTAINMENT PROTOCOL",
                "WARNING.\n"
                "BIOLOGICAL HAZARD PRECAUTION IN EFFECT.\n"
                "ALL QUARANTINE SEALS ENGAGED.\n"
                "UNAUTHORIZED ENTRY CONSTITUTES A BREACH OF UA REGULATION 364-A.8.\n",
                sound="rattle")
        # Run the menu
        simple_menu.run()

    def _display_warning(self, warning, sound="horn"):
        self.terminal.wait(0.25)
        self.terminal.play_sound("horn")
        while(True):
            self.terminal.print_instant(warning)
            user_input = input('\n»  ')
            self.terminal.clear()
            if user_input.lower() not in ["y","yes"]:
                self.terminal.play_sound("rattle")
            else:
                break

    def _run_apollo(self):
        self.terminal.clear()
        self._display_warning(
             "WARNING: YOU ARE ACCESSING A CLASSIFIED MILITARY SYSTEM.\n\n"
             "ACCESS WILL BE LOGGED.\n\n"
             "PROCEED? (Y/N)")
        self.terminal.wait(1)
        self.terminal.play_sound("beep")
        self.terminal.print_noise_screen(2)
        self.terminal.clear()
        self.terminal.play_sound("boot")
        self.terminal.print_instant(self.logo)
        self.terminal.wait(3)
        self.terminal.print_slow(self.boot_text, self.config.get("intro_speed"))
        self.terminal.wait(3)
        self.terminal.clear()
        self.terminal.print_slow("INTERFACE READY FOR INQUIRY.\nTERMINAL ACCESS GRANTED.")
        self.terminal.wait(2)
        self.terminal.clear()
        self.terminal.print_noise_screen(0.5)

    def play_intro(self):
        if self.config.get("power_online"):
            self._display_warning(
                "PROCEDURAL ANOMALY DETECTED IN REACTOR INITIATION.\n\n"
                "PER UNITED AMERICAS REGULATION 34.7,\n"
                "FILL OUT MAINTENANCE REPORT A12.\n\n"
                "PENALTIES APPLY FOR NON-COMPLIANCE.\nACKNOWLEDGE? (Y/N)")
        self._run_bios()
        self._run_apollo()
