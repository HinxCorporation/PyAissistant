import logging

import requests
from openai import OpenAI

from .chat_api import HinxtonChatBot
from .chat_bot_util import *
from .deep_seek_message_process import DeepSeekMessage


def expose_local_proxy():
    os.environ["http_proxy"] = "http://localhost:7890"
    os.environ["https_proxy"] = "http://localhost:7890"


def clear_local_proxy():
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""


def print_words(word: str):
    print(word, end='', flush=True)


class DeepSeekOpenAI(HinxtonChatBot):

    def __init__(self,
                 post_words=print_words,
                 function_call_feat=False,
                 custom_host=None,
                 custom_key=None,
                 custom_model=None,
                 custom_max_tokens=None,
                 custom_temperature=None,
                 custom_payloads=None):
        super().__init__(post_words, function_call_feat)
        if custom_host is not None:
            self.host = custom_host
        if custom_key is not None:
            self.key = custom_key
        self.client = OpenAI(
            api_key=self.key,
            base_url=self.host,
        )
        if custom_model is not None:
            self.model = custom_model
        if custom_max_tokens is not None:
            self.max_tokens = custom_max_tokens
        if custom_temperature is not None:
            self.temperature = custom_temperature
        if custom_payloads is not None:
            self.custom_payloads = custom_payloads
        else:
            self.custom_payloads = None

    def _finish_openai_payload(self, chain):
        if self.function_call_features:
            tools_exists = self.tools is not None and len(self.tools) > 0
            if tools_exists:
                return {
                    "messages": chain,
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "stream": self.stream,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "tools": self.tools,
                    "tool_choice": 'auto'
                }
        return {
            "messages": chain,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

    def _self_continue(self):
        response_text = ''
        uuid_tex: str = ''
        message_func = DeepSeekMessage()
        try:
            messages = self.message_chain()
            payload = self._finish_openai_payload(messages)
            if self.custom_payloads is not None:
                payload.update(self.custom_payloads)
            stream = self.client.chat.completions.create(**payload)
            for response in stream:
                # print(, end='')
                w = response.choices[0].delta.content
                if not uuid_tex:
                    uuid_tex = response.id
                message_func.process_open_ai_response(response)
                if w is not None:
                    self._write_out(w)
                    response_text += w
                else:
                    # self._write_out('.')
                    pass
        except requests.exceptions.RequestException as e:
            print(e)
            logging.error(f"Request error: {e}")
            raise e
        except Exception as e:
            print(e)
            logging.error(f"Error: {e}")
            raise e
        if not uuid_tex:
            uuid_tex = generate_uuid(32)
        extra = message_func.get_extras()
        return response_text, uuid_tex, {"function_calls": extra}
