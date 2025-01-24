import os

from muthur_gpt import constants


class PathResolver():
    """
    Path resolver to resolve path to resources.
    Checks plugin resources first, then base resources if not found.
    """
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        lib_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.normpath(os.path.join(lib_dir, ".."))
        # Order of path resolution:
        self.resource_resolve_path = [
            self._plugin_resource_root, self._base_resource_root]

    @property
    def _base_resource_root(self):
        return os.path.join(
            self.project_root,
            constants.RESOURCE_DIR)

    @property
    def _plugin_resource_root(self):
        return os.path.join(
            self.project_root,
            constants.PLUGIN_DIR,
            self.plugin_name,
            constants.RESOURCE_DIR)

    def _get_resource_path(self, relative_path):
        """
        Returns path to resource. None if not found.
        """
        # Resolve order
        for resource_dir in self.resource_resolve_path:
            resource_path = os.path.join(resource_dir, relative_path)
            # TODO make resource path case insensitive for name and ext?
            if os.path.exists(resource_path):
                return resource_path
        return None

    def get_sound_path(self, name):
        name += constants.SOUND_EXT
        return self._get_resource_path(os.path.join(constants.SOUND_DIR, name))

    def get_ascii_path(self, name):
        name += constants.ASCII_IMAGE_EXT
        return self._get_resource_path(os.path.join(constants.ASCII_DIR, name))

    def get_prompt_path(self, name):
        name += constants.PROMPT_EXT
        return self._get_resource_path(os.path.join(constants.PROMPT_DIR, name))

    def get_global_config_path(self):
        return os.path.join(
            self.project_root, constants.CONFIG_NAME + constants.CONFIG_EXT)

    def get_plugin_config_path(self):
        return os.path.join(
            self.project_root, constants.PLUGIN_DIR, self.plugin_name,
            constants.CONFIG_NAME + constants.CONFIG_EXT)
