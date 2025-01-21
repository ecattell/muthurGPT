from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

CODE="MANTICORE3788"

CONTAINMENT_PROMPT = f"""\nCONTAINMENT PROTOCOL LOCKDOWN:
- Fort Nebraska is under containment protocol lockdown due to a containment breach on Sublevel 03. You have no details beyond that.
- On lockdown, no outer doors can be opened, nor can automated outer defenses be shut down.
- The climber car has security clamps in place that will prevent it from moving mechanically. You can unlock them, but it will be a breach of the containment protocal.
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
        with open(self.path_resolver.get_ascii_path("CONTAINMENT_TEXT"), "r") as f:
            self.containment_text = f.read()

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

    def play_intro(self):
        self.terminal.wait(3)
        warnings = [
            "POWER CYCLE COMPLETED.\n\nLAUNCH MAINFRAME CORE? (Y/N)",
            "MAINTENANCE OPS INCOMPLETE. POSSIBLE FAULTS AHEAD.\n\nRESUME BOOT? (Y/N)",
            "PROCEDURAL ANOMALY DETECTED IN REACTOR INITIATION.\n\nPER UNITED AMERICAS REGULATION 34.7,\nFILL OUT MAINTENANCE REPORT A12.\n\nPENALTIES APPLY FOR NON-COMPLIANCE.\nACKNOWLEDGE? (Y/N)",
            "WARNING: YOU ARE ACCESSING A CLASSIFIED MILITARY SYSTEM.\n\nACCESS WILL BE LOGGED.\n\nPROCEED? (Y/N)"]

        for i, warning in enumerate(warnings):
            if i < len(warnings)-1:
                self.terminal.wait(.5)
                self.terminal.play_sound("horn")
            else:  # Handle last warning differently
                self.terminal.wait(1)
                self.terminal.play_sound("rattle")
            while(True):
                self.terminal.print_instant(warning)
                user_input = input('\n»  ')
                self.terminal.clear()
                if user_input.lower() not in ["y","yes"]:
                    self.terminal.play_sound("rattle")
                else:
                    break

            while(user_input.lower() not in ["y","yes"]):
                self.terminal.print_instant(warning)
                user_input = input('\n»  ')
                self.terminal.clear()

        self.terminal.wait(1)
        self.terminal.play_sound("beep")
        self.terminal.print_noise_screen(2)
        self.terminal.clear()
        self.terminal.play_sound("boot")
        self.terminal.print_instant(self.logo)
        self.terminal.wait(3)
        self.terminal.print_slow(self.boot_text, self.config.get("intro_speed"))
        self.terminal.wait(1)
        self.terminal.clear()
        self.terminal.play_sound("horn")
        self.terminal.wait(1)
        self.terminal.print_slow(self.containment_text, self.config.get("intro_speed"))
        self.terminal.play_sound("rattle")
        while(True):
            user_input = input('\n»  ')
            self.terminal.clear()
            if user_input.lower() not in ["y","yes"]:
                self.terminal.print_instant(self.containment_text)
                self.terminal.play_sound("rattle")
            else:
                break

        self.terminal.clear()
        self.terminal.print_slow("INTERFACE READY FOR INQUIRY.\nTERMINAL ACCESS GRANTED.")
        self.terminal.wait(2)
        self.terminal.clear()
        self.terminal.print_noise_screen(0.5)
