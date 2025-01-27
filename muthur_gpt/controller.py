import json
import os.path
from datetime import datetime

from muthur_gpt import app_config
from muthur_gpt import bots
from muthur_gpt import constants
from muthur_gpt import muthur_terminal
from muthur_gpt import path_utils
from muthur_gpt import plugin_base


class MuthurController():
    """
    Controls main MU/TH/UR cycle
    """
    def __init__(self, config, path_resolver, terminal, plugin, bot):
        self.config = config
        self.path_resolver = path_resolver
        self.terminal = terminal
        self.plugin = plugin
        self.bot = bot
        self.plugin_name = plugin.get_name()

    def run(self):
        # Play intro
        self.terminal.clear()
        if not self.config.get(constants.CONFIG_KEY_SKIP_INTRO):
            self.plugin.play_intro()

        # Loop to interactively ask questions from the terminal
        user_input = ''
        try:
            while True:
                self.terminal.clear()
                if user_input.startswith("!"):
                    self.terminal.print_header("Admin panel")
                    self.handle_command(user_input)
                else:
                    self.terminal.print_header()
                    self.plugin.draw_secondary_header()  # [plugin only, optional]
                    self.terminal.print_previous_input(user_input)
                    # Get reply from bot
                    if user_input:
                        # Filter input before sending to bot [plugin only, optional]
                        user_input = self.plugin.filter_user_input(user_input)
                        bot_reply = self.bot.get_reply(user_input)
                    else:
                        # This is either the first message or there is no user input.
                        bot_reply = self.config.get(constants.CONFIG_KEY_GENERIC_BOT_MESSAGE)

                    # Filter bot reply [plugin only, optional]
                    bot_reply = self.plugin.filter_bot_reply(bot_reply)

                    # Display reply
                    self.terminal.print_reply(bot_reply)

                # Prompt user for input
                user_input = self.terminal.get_input()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected.")
            self.config.save(name=f'{self.plugin.get_name()}_{datetime.now().strftime("%Y-%m-%d-%H-%M")}')
            print()

    def handle_command(self, command: str):
        if command.startswith("!exit"):
            print("Exiting MU/TH/UR....")  # implement saves!
            exit()
        elif command.startswith("!print"):
            parts = command.split()
            if len(parts) == 1:
                print("Printing the configuration")
                print(json.dumps(self.config.config, indent=4))
            elif len(parts) == 2:
                key = parts[1].replace('"', "").replace("'", "")
                value = self.config.get(key, None)
                if value is not None:
                    print(f"{key}: {value}")
                else:
                    print(f"Key '{key}' not found in configuration.")
        elif command.startswith("!set"):
            parts = command.split()
            if len(parts) == 3:
                self.config.set(parts[1], parts[2])
                try:
                    self.reload_bot()
                except Exception as e:
                    print(f"Failed to reload plugin: {e}")
            elif len(parts) == 4:
                self.config.set(parts[1], parts[2], parts[3])
                try:
                    self.reload_bot()
                except Exception as e:
                    print(f"Failed to reload plugin: {e}")
            else:
                print(f"Invalid command")
        elif command.startswith("!save"):
            parts = command.split()
            if len(parts) == 1:
                self.config.save()
            if len(parts) == 2:
                name = parts[1]
                self.config.save(name)
        else:
            print(f"Command {command} not implemented")

    def reload_bot(self):
        print('Attempting to reload chatbot')
        if self.config.get(constants.CONFIG_KEY_DEBUG):
            print('Reloading test bot')
            self.bot = bots.TestBot(self.plugin)
        else:
            print('Reloading GPT bot')
            self.bot = bots.GPTBot(self.plugin.build_prompt(), self.config)
        print('ChatBot reloaded successfully')

    @staticmethod
    def create_from_args(args):
        config = {}
        if args.save_file:
            muthur_lib = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
            save_file_path = os.path.join(muthur_lib, constants.SAVES_DIR, args.save_file + constants.SAVE_EXT)
            if not os.path.exists(save_file_path):
                raise FileNotFoundError(f"Savefile {args.save_file}{constants.SAVE_EXT} not found")
            else:
                print(f"Loading save file {args.save_file} ....")
                """
                Loading savefile data
                """
                with open(save_file_path, "r") as file:
                    save_file_data = json.load(file)
                args.plugin_name = save_file_data['plugin']
                config = app_config.Config(args.plugin_name, save_file_data['saved_config'])

        path_resolver = path_utils.PathResolver(args.plugin_name)  # regardless of savefile
        if not args.save_file:
            config = app_config.Config(args.plugin_name)
        terminal = muthur_terminal.MuthurTerminal(config, path_resolver, args.mute)
        plugin = plugin_base.Plugin.create_plugin(
            args.plugin_name, config, terminal, path_resolver)  # regardless of savefile
        bot = bots.ChatBot.create_bot(args, config, plugin)  # regardless of savefile
        return MuthurController(config, path_resolver, terminal, plugin, bot)
