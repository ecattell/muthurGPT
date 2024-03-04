OVERVIEW:
This is a chat bot that you can use to simulate an onboard computer such as MUTHUR for Alien RPG or other sci-fi tabletop role playing gamings.

It runs via OpenAI's API, and requires that you make a paid account with them to run. These are charged by OpenAI per token.

TERMINAL EMULATOR:
This package outputs directly to stdout. I recommend running this on a terminal with a scanline aesthetic, such as cool-retro-terminal.

I recommend using a rather large terminal font size to get the right look. The included ascii art assumes a minimum terminal width of 64 characters. That said, I wouldn't recommend going higher than 100. I usually run it with a width of 64.

INSTALLATION:
This is all python, so installation is pretty straightforward.

1) Update the config with your openAI API key.
2) Until you get your look right, I recommend specifying "debug=true" in the config so that it doesn't access openAI while you're iterating on cool-retro-terminal settings/etc.
3) At the muthur script in the bin dir to your path or just run it directly. Run "muthur --plugin cronus" for the Cronus' onboard MU/TH/UR or "muthur --plugin montero" for the montero

To be honest, I haven't attempted to run this from another machine yet, so I might have missed some steps. Because I'm doing sound in a dumb way for now, it will be mac dependant unless you update play_sound in terminal.py

CONFIG:
Take a look at the config to see what is configurable.

Each plugin can have their own overrides in the config. When running in the context of a plugin, values will be used instead of the config defaults if both exist. For a simple example, you could overwrite the title bar with different version of MU/TH/UR.

OPENAI API KEY:
The API key can be set either via environment variable (OPENAI_API_KEY) or via the config key "openai_api_key". I would suggest the former for safety, but the latter can be used to simplify setup. I would recommend disabling auto-refill on your account balance, and only adding money incrementally.

WHAT IS A PLUGIN?:
A plugin in muthurGPT can be loaded to initialize MU/TH/UR in different contexts. For example, on the Cronus or Montero in Chariot of the Gods. I've designed this package to allow new plugins to be installed without reinventing the wheel.

HOW TO INSTALL PLUGINS:
- Drag and drop the new plugin directory in your muthur_plugins directory.
- Only do so from trusted sources, since this will be running with your OpenAI key.

HOW TO CREATE PLUGINS:
- You can quickly add additional story contexts beyond the Cronus/Montero for MU/TH/UR to run in.
- Duplicate the muthur_plugins/template directory, and rename it to a name of your choice.
- Update and rename the copied "template_prompt.txt" to include whatever scenario-specific information MU/TH/UR needs to have. (and rename it to <YOURNAME>_prompt.txt)
- In the copied template version of "__init__.py", rename TemplatePlugins to <YOURNAME>Plugin and update NAME to be <YOURNAME>.
- You're good to go! If you want to do advanced behavior, such as filtering input/output from GPT to use special tokens / maps, etc, then you can use the Cronus as an example. Otherwise, Montero is a simpler starting point.

OUTSTANDING WORK (in vague order of priority):
- Output sound in less dumb way.
- Allow for user to quit MUTHUR from within MUTHUR using natural language.
- Output log as save. Allow program to be continued from save file.
- Make prompts configurable with string replacements.
- Add standardized variant definitions in config for plugins.
- Have two streams --- one for stdout/debugging one for MUTHUR.
- Write simple unit tests, especially for plugin dev.