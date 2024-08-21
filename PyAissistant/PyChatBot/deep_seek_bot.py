import configparser
import logging
import webbrowser

import requests

from .chat_api import HinxtonChatBot
from .chat_bot_util import *
from .deep_seek_message_process import DeepSeekMessage
from ..Extension.ai_extension import *


class DeepSeekBot(HinxtonChatBot):

    @staticmethod
    def open_browser(url):
        # Open the URL in the default web browser
        webbrowser.open(url)

    @staticmethod
    def call_user_by_name(name):
        # Call the user by name
        return f'call {name} success, job done'

    def __init__(self, post_words=print_words, function_call_feat=False):
        super().__init__(post_words, function_call_feat)
        config_file = 'config.ini'
        config = configparser.ConfigParser()
        try:
            config.read(config_file, encoding='utf-8')
            current = config.get('ai', 'current')

            self.cache_transitions = config.getboolean("setting", "cache_transitions", fallback=False)
            self.use_proxy = config.getboolean("setting", "use_proxy", fallback=False)
            self.proxy_uri = config.get("setting", "proxy", fallback='')
            print('AI(Deep Seek Tips):', current, self.url)
            if self.use_proxy:
                print('using Proxy:', self.proxy_uri)

        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            logging.error(f"Error reading config file: {e}")
            raise

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
        self.block_mark = 'data:'

    def setup_function_tools(self):
        functions = self._get_demo_functions()
        functions.extend(list_exposed_functions())
        self.executor.extend_tools(functions)

    def _get_demo_functions(self):
        return [self.open_browser, self.call_user_by_name]

    def create_request(self, **kwargs):
        if self.use_proxy:
            return requests.request("POST", self.url, stream=True, proxies={"https": self.proxy_uri, }, **kwargs)
        else:
            return requests.request("POST", self.url, stream=True, proxies={"http": "", "https": ""}, **kwargs)

    def go_next(self, content: str):
        # find the first block
        position = content.find(self.block_mark)
        if position != -1:
            current_line = content[:position].strip()
            rest_content = content[position + len(self.block_mark):]
            return current_line, rest_content
        return '', content

    def _finish_deep_seek_payload(self, chain):
        # Configuring function calling behavior using the tool_choice parameter By default, the model is configured
        # to automatically select which functions to call, as determined by the tool_choice: "auto" setting. We offer
        # three ways to customize the default behavior: To force the model to always call one or more functions,
        # you can set tool_choice: "required". The model will then always select one or more function(s) to call.
        # This is useful for example if you want the model to pick between multiple actions to perform next. To force
        # the model to call a specific function, you can set tool_choice: {"type": "function", "function": {"name":
        # "my_function"}}. To disable function calling and force the model to only generate a user-facing message,
        # you can either provide no tools, or set tool_choice: "none".
        if self.function_call_features:
            tools_exists = self.tools is not None and len(self.tools) > 0
            if tools_exists:
                return json.dumps({
                    "messages": chain,
                    "model": self.model,
                    "frequency_penalty": 0,
                    "max_tokens": self.max_tokens,
                    "presence_penalty": 0,
                    "stop": None,  # stop continue while this word is generated
                    "stream": self.stream,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "tools": self.tools,
                    "tool_choice": 'auto',
                    "logprobs": False,
                    "top_logprobs": None
                })
        return json.dumps({
            "messages": chain,
            "model": self.model,
            "frequency_penalty": 0,
            "max_tokens": self.max_tokens,
            "presence_penalty": 0,
            "stop": None,  # stop continue while this word is generated
            "stream": self.stream,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "tools": None,
            "tool_choice": "none",
            "logprobs": False,
            "top_logprobs": None
        })

    def _self_continue(self):
        # response = self.client.request_completion(model="llama3.1", stream=True, prompt=message)
        chain = self.message_chain()
        payload = self._finish_deep_seek_payload(chain)
        if self.cache_transitions:
            with open('payload.json', 'w', encoding='utf-8') as f:
                f.write(payload)
        response_text = ""
        msg_stack = ""
        message_func = DeepSeekMessage()
        try:
            response = self.create_request(headers=self.headers, data=payload)
            response.raise_for_status()
            response_f = None
            if self.cache_transitions:
                response_f = open('response.json', 'wb')
            for chunk in response.iter_content(chunk_size=1024):
                if self.cache_transitions:
                    response_f.write(chunk)
                chunk_text = chunk.decode('utf-8')  # Decode bytes to string
                msg_stack += chunk_text
                # process every block
                while msg_stack and self.block_mark in msg_stack:
                    # msg_stack, w = self.try_outline(msg_stack)
                    # response_text += w
                    line, msg_stack = self.go_next(msg_stack)
                    if line:
                        w = message_func.process_new_line(line)
                        if w is not None:
                            self._write_out(w)
                            response_text += w
            if response_f:
                response_f.close()

        except requests.exceptions.RequestException as e:
            print(e)
            logging.error(f"Request error: {e}")
            raise e
        except Exception as e:
            print(e)
            logging.error(f"Error: {e}")
            raise e

        # from message stack line 0 read id
        try:
            first_line = msg_stack.splitlines()[0][len(self.block_mark) + 1:]
            json_data = json.loads(first_line)
            uuid_tex = json_data.get('id')
        except:
            uuid_tex = generate_uuid(32)
        extra = message_func.get_extras()
        return response_text, uuid_tex, {"function_calls": extra}
