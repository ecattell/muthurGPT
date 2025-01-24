import json
import os
from muthur_gpt import path_utils
from muthur_gpt import constants
from datetime import datetime


class Config:
    """
    Config class to handle global and plugin-specific configurations.
    Allows plugins to override values with matching keys.
    """

    def __init__(self, plugin_name=None, save_file_config=None):
        path_resolver = path_utils.PathResolver(plugin_name)
        self.plugin_name = plugin_name
        if save_file_config is None:
            # Load the main (global) configuration
            with open(path_resolver.get_global_config_path(), "r") as file:
                self.config = json.load(file)

            # If a plugin name is provided, attempt to load its specific configuration
            if plugin_name:
                plugin_config_path = path_resolver.get_plugin_config_path()
                if os.path.exists(plugin_config_path):
                    with open(plugin_config_path, "r") as plugin_file:
                        plugin_config = json.load(plugin_file)

                    # Merge plugin config, prioritizing plugin-specific keys
                    self.config = self._merge_configs(self.config, plugin_config)
        else:
            with open(path_resolver.get_global_config_path(), "r") as file:
                base_config = json.load(file)
            self.config = save_file_config
            """
            Keys that are not in the savefile will be supplemented from the main config.json
            """

            keys_to_supply = [
                'debug', 'skip_intro', 'openai_model', 'openai_api_key', 'default_speed',
                'map_speed', 'prompt_wait_time', 'generic_bot_message', 'text_to_speech',
                'misc_addendums', 'force_upper_case']  # to do - merge with keys_to_remove
            for key in keys_to_supply:
                if key not in self.config:
                    self.config[key] = base_config[key]

    def _merge_configs(self, base_config, override_config):
        """
        Recursively merge two configurations, where override_config takes precedence.
        """
        for key, value in override_config.items():
            if (
                key in base_config
                and isinstance(base_config[key], dict)
                and isinstance(value, dict)
            ):
                # If both values are dictionaries, merge them recursively
                base_config[key] = self._merge_configs(base_config[key], value)
            else:
                # Otherwise, override the base value
                base_config[key] = value
        return base_config

    def get(self, key, default=None):
        """
        Retrieve a configuration value.
        Priority: plugin-specific -> global -> default.
        """
        if self.plugin_name:
            plugin_config = self.config.get("plugins", {}).get(self.plugin_name, {})
            if key in plugin_config:
                return plugin_config[key]

        # Fallback to global configuration
        return self.config.get(key, default)

    def set(self, key, value, set_new: bool = False):
        """
        Overwrite a value in the config with a new value.
        Will print a warning if the key is not found within config, unless "set_new" is True.
        """
        key = ensure_double_quotes(key).strip('"')  # Ensure the key is clean

        if value is True or value is False:
            value = value
        elif isinstance(value, str) and value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
            value = int(value)
        elif (
            value.replace('.', '', 1).isdigit()
            or (value[0] == '-' and value[1:].replace('.', '', 1).isdigit())
        ):
            value = float(value)
        else:
            value = value.strip("'\"")  # Store the clean string directly

        if key in self.config:
            self.config[key] = value
            print(f'{key} set to {value}')
        elif set_new:
            self.config[key] = value
            print(f'Created a new key - {key} and set it to {value}')
        else:
            print(
                f"{key} not found in the config. "
                f"If you want to add the value regardless, then add a third argument - True"
            )

    def save(self, name=None):
        """
        Save current config as a save to be later reloaded.
        If a save file with the given name exists, append a unique number like (1), (2), etc.
        """
        # Generate a default name if none is provided
        if name is None:
            name = f'{self.plugin_name.name}_{datetime.now().strftime("%Y-%m-%d-%H-%M")}'

        # Path to save directory
        saves_dir_path = os.path.join(
            path_utils.PathResolver(self.plugin_name).project_root,
            constants.SAVES_DIR
        )
        os.makedirs(saves_dir_path, exist_ok=True)  # Ensure the directory exists

        # Initial save file path
        base_file_name = str(name) + constants.SAVE_EXT
        save_file_path = os.path.join(saves_dir_path, base_file_name)

        # If the file already exists, add a number (e.g., "name(1).ext")
        counter = 1
        while os.path.exists(save_file_path):
            file_name_with_counter = f"{name}({counter}){constants.SAVE_EXT}"
            save_file_path = os.path.join(saves_dir_path, file_name_with_counter)
            counter += 1

        # Create a modified config before saving
        keys_to_remove = [
            'debug', 'skip_intro', 'openai_model', 'openai_api_key', 'default_speed',
            'map_speed', 'prompt_wait_time', 'generic_bot_message', 'text_to_speech',
            'misc_addendums', 'force_upper_case'
        ]
        cleaned_config = {k: v for k, v in self.config.items() if k not in keys_to_remove}

        # Add "plugin" and current time to the cleaned config
        modified_config = {
            "plugin": self.plugin_name,
            "timestamp": datetime.now().strftime("%y-%m-%d-%H-%M-%S"),
            "saved_config": cleaned_config
        }

        # Save the modified configuration to the file
        with open(save_file_path, "w") as save_file:
            json.dump(modified_config, save_file, indent=4)

        print(f"Configuration saved as: {save_file_path}")


def ensure_double_quotes(value):
    """
    Strip any existing quotes (single or double) and wrap with double quotes.
    """
    stripped_value = value.strip("'\"")
    return f'"{stripped_value}"'


# Example usage
if __name__ == "__main__":
    config = Config("cronus")

    # Accessing a configuration value
    print(f"Printing config for {config.plugin_name}\n{config.config}")
    config.set("debug", True)
    print(config.config)
    config.set("engine_status", "working fine")
    print(config.config)
    config.set("engine_status", "working fine", True)
    print(config.config)
    config.save()
