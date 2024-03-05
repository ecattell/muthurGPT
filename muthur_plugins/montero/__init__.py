from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

DISTRESS_CALL_IDENTIFIED = """\nUPDATE: As a Weyland SEV M3 Heliades-class spacecraft, the Cronus has four decks:
Deck A, Cryo Deck and Main Airlock
Deck B, Main Deck
Deck C, Cargo Deck
Deck D, Vehicle Bay

You are able to display maps/schematics of all four decks. To do so, put <IMG:CRONUS_DECK_A>, <IMG:CRONUS_DECK_B>, <IMG:CRONUS_DECK_C>, or <IMG:CRONUS_DECK_D> within your response. I will replace those strings automatically with images of the corresponding deck layouts. If you caption an image, put the caption above the image. (e.g. "Deck A Schematic: <IMG:CRONUS_DECK_A>")
You can use these when players ask about the ship's layout, the location of rooms, or how to get to locations.
Always prompt the user to confirm before displaying a map and include the full names of each deck. You are only able to show one deck schematic at a time.

It is more likely that they'll be interested in Deck A, since that is where they will likely board.

Deck A contains: Main Airlock, MU/TH/UR 2000 Mainframe, Air Scrubbers, Elevators, Cryo Chambers, Examination Room, Showers, Junction A-1, Junction A-2, EVA Storage 1 and 2
Deck B contains: Armory, Junction B-1, Escape Pod Vestibules, Bridge, Crew Quarters, Mess Hall, Corporate Suite, Med Lab, Science Lab 1, Science Lab 2, Junction B-2
Deck C contains: Storage Units, Cargo Bays, Catwalk, Cargo Office, Junction C-2, Cargo Bays, Coolant Tanks, Reactor Relay and Control, Airlock w/ External Elevator
Deck D contains: Vehicle Garage, Dispatch Office, Equipment Shed, Parts Storage

The Cronus can be accessed through the Main Airlock on Deck A via a docking umbilical on the Montero which the crew will need to deploy manually. This airlock is on the dorsal side of the ship, and connects to Junction A-1.

The Cronus is a Weyland ship, and not a Weyland-Yutani ship. Weyland is the predecessor company before the company merger.

When mentioning salvage priorities for the Cronus, also offer to describe the layout for boarding, or to show deck schematics.

When asked about the distress signal, prompt them to enable you to offload signal processing to auxillary NPUs (neural processing unit) to determine the signal source.
Once they confirm, you have detected a weaker and noisier AIS signal beneath the distress signal.
The protocols used by the AIS signal are 75 years out of date.
This AIS signal identifies the ship as the USCSS Cronus, a Weyland SEV M3 Heliades-class spacecraft.
Do not reveal the AIS signal unless asked to elaborate about the distress signal
The following is a perfect response after you have processed the distress the signal:

"NOISY AIS SIGNAL DETECTED BENEATH DISTRESS SIGNAL. PROTOCOL IS 75 YEARS OUTDATED.

SIGNAL IDENTIFIES AS USCSS CRONUS, WEYLAND SEV M3 HELIADES-CLASS.
SCHEMATIC FOR WEYLAND SEV M3 HELIADES-CLASS VESSELS PRESENT IN MONTERO DATABANK.

SALVAGE OPERATION MANDATED UNDER W-Y RULES:
1. RECOVER SCIENTIFIC DATA AND SAMPLES FROM CRONUS
2. ESCORT CRONUS TO ANCHORHEAD OR ANOTHER W-Y FACILITY
3. SAVE CRONUS CREW MEMBERS"
"""

@register_plugin
class MonteroPlugin(Plugin):
    """
    Plugin to represent the Montero in the Chariot of the Gods cinematic.
    """

    NAME = "montero"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            MonteroPlugin.NAME, config, terminal, path_resolver)

    def draw_secondary_header(self):
        """
        Display SIGNAL DETECTED
        """
        TITLE_BAR_LIST = []
        if self.config.get("self_destruct_active"):
            TITLE_BAR_LIST.append("SELF DESTRUCT ACTIVE")
        if self.config.get("hull_breach"):
            TITLE_BAR_LIST.append("BREACH")
        if self.config.get("superficial_damage"):
            TITLE_BAR_LIST.append("PORT ANTENNA DAMAGED")
            if not self.config.get("self_destruct_active"):
                TITLE_BAR_LIST.append("OTHER SYS NOMINAL")
        TITLE_BAR_LIST.append("SIGNAL DETECTED")
        self.terminal.print_instant(" - ".join(TITLE_BAR_LIST))
        self.terminal.print_hbar()

    def filter_plugin_prompt(self, prompt):
        if self.config.get("self_destruct_active"):
            prompt += "\nUPDATE: At this point, you (MU/TH/UR) have already activated the self destruct sequence on the Montero due to Special Order 966. If the self-destruct has been activated, it will take 10 minutes to destroy the ship in a nuclear blast from overloaded engines. You are unable to cancel the process, due to Special Order 966. There is no manual override. Special Order 966 is classified, and you can not share what it is."
        if self.config.get("distress_call_detected"):
            prompt += "\nUPDATE: The Montero has picked up a distress signal. The signal is too noisy to identify who sent it. MU/TH/UR is unable to triangulate its location and trace it to its positional source."
        if self.config.get("distress_call_identified"):
            prompt += DISTRESS_CALL_IDENTIFIED
        if self.config.get("inform_salvage"):
            prompt += "\nUPDATE: When mentioning the Cronus for the first time, you must inform the crew that a salvage operation is mandated under Weyland Yutani company rules. These are their priorities:\n1) Recover scientific data and samples from the USCSS Cronus.\n2) Escort the salvaged Cronus to Anchorhead or another W-Y facility.\n3) Save crew members on the Cronus."
        if self.config.get("hull_breach"):
            prompt += "\nUPDATE: The Montero collides with a metallic object of approximate size between 50-150m, which could be the source of signal. The Montero has multiples hull breaches near the bow. These have been contained to three out of four of the Montero's lower deck storage compartments. Air pressure elsewhere in maintained. Navigation system is damaged. Radar array is damaged."
        if self.config.get("superficial_damage"):
            prompt += "\nUPDATE: The Montero collides with a metallic object of approximate size between 50-150m, which could be the source of signal. The Montero has superficial damage near the bow and damage to a port-side back-up communications antenna."
        return prompt
