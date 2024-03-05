import importlib
import pkgutil
import os

def get_plugin_subdirs(plugin_root_dir):
    plugin_dirs = []
    for item in os.listdir(plugin_root_dir):
        item_path = os.path.join(plugin_root_dir, item)
        if os.path.isdir(item_path):
            plugin_dirs.append(item_path)
    return plugin_dirs

def load_plugins():
    """
    Dynamically import all plugin modules under plugins package
    """
    import muthur_plugins
    plugin_root_dir = muthur_plugins.__path__[0]
    for _, plugin_name, _ in pkgutil.iter_modules([plugin_root_dir]):
        rel_dir = os.path.relpath(plugin_root_dir, plugin_root_dir)
        module_name = '.'.join(["muthur_plugins", plugin_name])
        importlib.import_module(module_name)
