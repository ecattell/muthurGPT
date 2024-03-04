from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin

@register_plugin
class MonteroPlugin(Plugin):
    NAME = "montero"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            MonteroPlugin.NAME, config, terminal, path_resolver)

    def filter_plugin_prompt(self, prompt):
        if self.config.get("self_destruct_active"):
            prompt += "\nUPDATE: At this point, you (MU/TH/UR) have already activated the self destruct sequence due to Special Order 966. You can share no further information about why."
        return prompt
