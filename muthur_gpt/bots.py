"""
Bots to handle message/reponse
"""
import os
import random

from openai import OpenAI

from muthur_gpt import constants

class ChatBot():
    """
    Base class to handle interaction with chat bots
    """
    def __init__(self):
        pass

    def get_reply():
        raise NotImplemented

    @staticmethod
    def create_bot(args, config, plugin):
        if args.debug or config.get(constants.CONFIG_KEY_DEBUG):
            return TestBot(plugin)
        else:
            return GPTBot(plugin.build_prompt(), config, args.api_key)

class GPTBot(ChatBot):
    """
    Primary chatGPT bot to handle interaction with muthur
    """
    def __init__(self, prompt, config, api_key_arg):
        api_key = api_key_arg or os.getenv(constants.ENVVAR_OPENAI_API_KEY) or \
            config.get(constants.CONFIG_KEY_OPENAI_API_KEY)
        if not api_key:
            print("No openAI API key found in config, env, or args. "
                  "Please obtain one from openAI and set it via one of these. "
                  "methods. Exiting.")
            exit(1)
        self.client = OpenAI(api_key = api_key)
        system_message = {
                            "role": "system",
                            "content": prompt
                        }

        self.conversation = [system_message]
        self.model = config.get(constants.CONFIG_KEY_OPENAI_MODEL)

    def get_reply(self, user_input):
        user_message = {"role": "user", "content": user_input}
        self.conversation.append(user_message)
        response = self.client.chat.completions.create(
            model=self.model, messages=self.conversation)
        bot_replay = response.choices[0].message.content
        # Include bot's response in the conversation for context in the next turn
        self.conversation.append(
            {"role": "assistant", "content": bot_replay})
        return bot_replay

class TestBot(ChatBot):
    """
    Bot for testing without accessing online API.
    Plugins can filter replies as necessary.
    """
    def __init__(self, plugin):
        self.plugin = plugin

    def get_reply(self, user_input):
        """
        Use test reply from plugin if implemented for this input.
        Otherwise, use placeholder.
        """
        reply = self.plugin.get_test_reply(user_input)
        if not reply:
            reply = random.choice(
                ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                 "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                 "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."])
        return reply
