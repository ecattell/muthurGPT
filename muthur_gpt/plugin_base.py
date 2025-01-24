from muthur_gpt import constants


class Plugin():
    """
    Base class for all plugins.
    Plugins alter the prompt and behavior of MU/TH/UR.

    Different plugins can be loaded in muthurGPT to initialize MU/TH/UR in
    different contexts. For example, different ships or different storylines.
    """
    def __init__(self, name, config, terminal, path_resolver):
        self.name = name
        self.config = config
        self.terminal = terminal
        self.path_resolver = path_resolver

    def get_name(self):
        return self.name

    def build_prompt(self):
        prompt_prefix_path = self.path_resolver.get_prompt_path(
            constants.PROMPT_PREFIX_NAME)
        prompt_suffix_path = self.path_resolver.get_prompt_path(
            constants.PROMPT_SUFFIX_NAME)
        plugin_prompt_path = self.path_resolver.get_prompt_path(
            f"{self.name}_prompt")

        # Validate that prompts all exist
        if not all([prompt_prefix_path, prompt_suffix_path, plugin_prompt_path]):
            print(f"Unable to find all prompt files.")
            exit(1)

        # Combine and filter prompts
        with open(prompt_prefix_path, "r") as f:
            prompt_prefix = f.read()
        with open(prompt_suffix_path, "r") as f:
            prompt_suffix = f.read()
        with open(plugin_prompt_path, "r") as f:
            plugin_prompt = self.filter_plugin_prompt(f.read())
        return "\n\n".join([prompt_prefix, plugin_prompt, prompt_suffix])

    def filter_plugin_prompt(self, plugin_prompt):
        """
        Can be optionally implemented by plugins to filter the plugin prompt.
        For example, it could add or change text based on config settings.
        """
        return plugin_prompt

    def draw_secondary_header(self):
        """
        Can be optionally implemented to add a second header immediately below
        the first to display information such as warnings/etc.
        """
        pass

    def play_intro(self):
        """
        Can be optionally implemented to display an intro when MU/TH/UR boots
        If this is unimplemented, we assume that an intro is not used.
        """
        pass

    def filter_bot_reply(self, bot_reply):
        """
        Can be optionally implemented to filter the bot_reply or to process
        it in some way. Should always return the bot_reply (or a modified
        version of it).

        For example, it could remove and process special tokens that your
        gpt prompt relies on that aren't intended to be seen by the user.
        Or it could just play sounds when specific words appear in the output.
        """
        return bot_reply

    def filter_user_input(self, user_input):
        """
        Can be optionally implemented to filter the user_input before it is
        sent to the bot. For example, to add special
        """
        return user_input

    def get_test_reply(self, user_input):
        """
        It's not required for plugins to implement a test reply.
        This allows some testing when not connected to OpenAI API.
        If plugin returns an empty response, it should be replaced with temp text.
        """
        return ""

    @staticmethod
    def create_plugin(name, config, terminal, path_resolver):
        if name not in all_plugins:
            raise Exception(
                "Plugin not recognized. "
                "Has it been added to all_plugins?")
        else:
            print(f"Plugin {name} recognized as it exists in {all_plugins}")

        return all_plugins[name](config, terminal, path_resolver)


# All plugins need to register themselves with this decorator
all_plugins = {}


def register_plugin(cls):
    """
    A decorator to register plugin classes
    """
    all_plugins[cls.NAME] = cls
    return cls
