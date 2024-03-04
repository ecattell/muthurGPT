from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

@register_plugin
class TemplatePlugin(Plugin):
    """
    This template plugin is intended to be used as an example of the most
    minimal possible plugin. Copy it to form the basis of a new plugin.
    """
    NAME = "template"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            TemplatePlugin.NAME, config, terminal, path_resolver)
