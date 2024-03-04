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

    def run(self):
        # Play intro
        self.terminal.clear()
        if not self.config.get(constants.CONFIG_KEY_SKIP_INTRO):
            self.plugin.play_intro()

        # Loop to interactively ask questions from the terminal
        user_input = ''
        while True:
            self.terminal.clear()
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

    @staticmethod
    def create_from_args(args):
        path_resolver = path_utils.PathResolver(args.plugin_name)
        config = app_config.Config(path_resolver.get_config_path(), args.plugin_name)
        terminal = muthur_terminal.MuthurTerminal(config, path_resolver)
        plugin = plugin_base.Plugin.create_plugin(
            args.plugin_name, config, terminal, path_resolver)
        bot = bots.ChatBot.create_bot(args, config, plugin)
        return MuthurController(config, path_resolver, terminal, plugin, bot)
