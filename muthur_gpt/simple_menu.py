"""
Simple helper classes for building minimal multiple choice interfaces that
don't use a chatbot.

For example, the BIOS interface in the Fort Nebraska plugin while A.P.O.L.L.O
is offline.
"""

class SimpleMenuItem():
    """
    Represents one item on the multiple choice menu list.
    """
    def __init__(self, title, message, sound, exit_query=None):
        """
        title: String for item's name in menu, as well as titlebar for item page
        message: String display on item page
        sound: Sound to play when opening item page
        exit_query: Ask this query and allows the user to exit this menu
        If exit_query not given, will only give option to return to root menu.
        """
        self.title = title
        self.message = message
        self.sound = sound
        self.exit_query = exit_query

class SimpleMenu():
    """
    A navigable collection of SimpleMenuItems
    """
    def __init__(self, terminal, header):
        self.terminal = terminal
        self.header = header
        self.menu_items=[]

    def add_option(self, title, message, sound=None, exit_query=None):
        """
        Adds a new menu item.
        """
        self.menu_items.append(SimpleMenuItem(title, message, sound, exit_query))

    def print_menu(self):
        """
        Displays the root menu
        """
        self.terminal.clear()
        self.terminal.print_header(header_override=self.header)
        for i, menu_item in enumerate(self.menu_items):
            self.terminal.print_slow(f"{i+1}) {menu_item.title}")

    def run(self):
        """
        Run the main loop of this simple menu until user exits via an "exit"
        item.
        """
        self.terminal.print_noise_screen(2)
        self.terminal.clear()
        while(True):
            self.print_menu()
            # Determine chosen menu item
            # First check if they used exact string match
            user_input = input('\n»  ').strip()
            chosen_item = None
            for menu_item in self.menu_items:
                if menu_item.title.lower() == user_input.lower():
                    chosen_item = menu_item
                    break
            # Next, check if they used an index
            if not chosen_item:
                try:
                    chosen_item = self.menu_items[int(user_input)-1]
                except (IndexError, TypeError, ValueError) as e:
                    # Give up, and wait for a new input
                    self.terminal.play_sound("rattle")
                    continue
            # Display menu item
            exit_chosen = self.run_item(chosen_item)
            if exit_chosen:
                return


    def run_item(self, menuItem):
        """
        The user has clicked on a specific menu item.
        Displays text, and asks the user if they wish to return to the menu.
        If menu item allows for exit, it can leave this menu system.
        """
        while(True):
            self.terminal.clear()
            self.terminal.print_header(header_override=self.header)
            if menuItem.sound:
                self.terminal.play_sound(menuItem.sound)
            self.terminal.print_instant(menuItem.title)
            self.terminal.print_hbar(character="░")
            self.terminal.print_slow(menuItem.message)
            self.terminal.print_hbar(character="░")
            if menuItem.exit_query:
                self.terminal.print_instant(menuItem.exit_query)
                user_input = input('\n»  ')
                if user_input.lower() in ["y","yes"]:
                    return True
                else:
                    return False
            else:
                self.terminal.print_instant("BACK? (Y/N)")
                user_input = input('\n»  ')
                if user_input.lower() in ["y","yes"]:
                    break
                else:
                    self.terminal.play_sound("rattle")
        return False