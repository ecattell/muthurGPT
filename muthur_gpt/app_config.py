import json

from muthur_gpt import constants

class Config():
    """
    Config which allows plugins to override values with matching keys
    """
    def __init__(self, config_path, plugin_name):
        with open(config_path, "r") as file:
            self.config = json.load(file)
            self.plugin_name = plugin_name

    def get(self, key, default=None):
        value = self.config.get(
            constants.CONFIG_KEY_PLUGIN, {}).get(self.plugin_name, {}).get(key)
        # Fall back to base config value
        if value is None:
            value = self.config.get(key)
        # Fall back to default if no key
        if value is None:
            value = default
        return value
