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

    def __init__(self, post_words=print_words, function_call_feat=False):
        super().__init__(post_words, function_call_feat)
        self.client = OpenAI(
            api_key=self.key,
            base_url=self.host,
        )

    def _finish_deep_seek_payload(self, chain):
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
        msg_stack = ""
        uuid_tex: str = ''
        message_func = DeepSeekMessage()
        try:
            messages = self.message_chain()
            stream = self.client.chat.completions.create(**self._finish_deep_seek_payload(messages))
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
                    pass
                    # self._write_out('.')

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
