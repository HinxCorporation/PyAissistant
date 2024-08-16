import configparser
import logging
import webbrowser

import requests

from .chat_api import ChatBot
from .chat_bot_util import *
from .deep_seek_message_process import DeepSeekMessage
from .. import ai_assist
from ..Extension.ai_extension import *


class DeepSeekBot(ChatBot):

    @staticmethod
    def open_browser(url):
        # Open the URL in the default web browser
        webbrowser.open(url)

    @staticmethod
    def call_user_by_name(name):
        # Call the user by name
        return f'call {name} success, job done'

    def __init__(self, post_words=print_words, function_call_feat=False):
        super().__init__(post_words)
        config_file = 'config.ini'
        config = configparser.ConfigParser()
        try:
            config.read(config_file, encoding='utf-8')
            current = config.get('ai', 'current')
            self.key = config.get(current, "key")
            self.url = config.get(current, "url")
            self.model = config.get(current, "current")
            self.cache_transitions = config.getboolean("setting", "cache_transitions", fallback=False)
            self.use_proxy = config.getboolean("setting", "use_proxy", fallback=False)
            self.proxy_uri = config.get("setting", "proxy", fallback='')
            print('AI(Deep Seek Tips):', current, self.url)
            if self.use_proxy:
                print('using Proxy:', self.proxy_uri)

            color_block_options = config.options('Colors')
            self.colors = dict()
            for key in color_block_options:
                self.colors[key] = config.get('Colors', key)

        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            logging.error(f"Error reading config file: {e}")
            raise

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
        self.stream = True  # open async stream
        self.block_mark = 'data:'
        self.max_tokens = 2048
        self.temperature = 1
        self.top_p = 1
        self.function_call_features = function_call_feat
        if function_call_feat:
            self.functions = [self.open_browser, self.call_user_by_name]
            self.append_global_exposed_functions()
            self.tools = [ai_assist.collect_function_as_tool(func) for func in self.functions]
        else:
            self.tools = []
            self.functions = []
        self.choices = []

    def append_global_exposed_functions(self):
        exposed_functions = list_exposed_functions()
        self.functions.extend(exposed_functions)

    def create_request(self, **kwargs):
        if self.use_proxy:
            return requests.request("POST", self.url, stream=True, proxies={"https": self.proxy_uri, }, **kwargs)
        else:
            return requests.request("POST", self.url, stream=True, proxies={"http": "", "https": ""}, **kwargs)

    def get_local_functions_by_name(self, method_name):
        for func in self.functions:
            if func.__name__ == method_name:
                return func
        return None

    def execute_func(self, function_tool, **kwargs):
        if not self.function_call_features:
            return ''
        tool_details = function_tool['function']
        function_name = tool_details['name']
        function_desc = tool_details['description']
        logging.info(f" - (ai) Executing function: {function_name} with args: {kwargs} , go for {function_desc}")
        matched_func = self.get_local_functions_by_name(function_name)
        if matched_func is not None:
            exec_result = matched_func(**kwargs)
            if exec_result is not None:
                logging.info(f" - (ai) Function {function_name} executed successfully, return value: {exec_result}")
                return exec_result
            else:
                logging.info(f" - (ai) Function {function_name} executed successfully, but no return value found.")
                return f"Function {function_name} successfully executed, but no return value found."
        else:
            logging.error(f" - (ai) Function not found: {function_name}")
            return None

    def go_next(self, content: str):
        # find the first block
        position = content.find(self.block_mark)
        if position != -1:
            current_line = content[:position].strip()
            rest_content = content[position + len(self.block_mark):]
            return current_line, rest_content
        return '', content

    def get_color(self, colorName):
        exist = self.colors.__contains__(colorName)
        if exist:
            color = self.colors[colorName]
        else:
            color = None
        return exist, color

    def _generate_response(self, user_input: str) -> [str, str, dict]:
        return self._self_continue()

    def _self_continue(self):
        # response = self.client.request_completion(model="llama3.1", stream=True, prompt=message)
        chain = self.message_chain()
        model = self.model
        payload = json.dumps({
            "messages": chain,
            "tools": self.tools,
            "model": model,
            "frequency_penalty": 0,
            "max_tokens": self.max_tokens,
            "presence_penalty": 0,
            "stop": None,  # stop continue while this word is generated
            "stream": self.stream,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "logprobs": False,
            "top_logprobs": None
        })
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
        except Exception as e:
            print(e)
            logging.error(f"Error: {e}")

        # from message stack line 0 read id
        try:
            first_line = msg_stack.splitlines()[0][len(self.block_mark) + 1:]
            json_data = json.loads(first_line)
            uuid_tex = json_data.get('id')
        except:
            uuid_tex = generate_uuid(32)
        # self._write_out('\n----------DEMO ENDS-----------\n')

        return response_text, uuid_tex, {"function_calls": message_func.get_extras()}
