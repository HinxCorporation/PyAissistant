import os

from colorama import Fore
from colorama import Style

from .__console_extend import greet, is_quit, process_ai_message, out_ai_role_msg, tips_out
from .chat_api import ChatBot
from .chat_bot_util import clear_console
from .deep_seek_bot import DeepSeekBot


class ConsoleChat:
    def __init__(self, bot: ChatBot = None, user_name="You", bot_name="Bot", system_name='system', fm_name='file'):
        self.bot_msg: str = ''
        # utils needs an output method with a token input
        self.bot: ChatBot
        if bot is not None:
            self.bot = bot
        else:
            self.bot = DeepSeekBot()
            # self.bot = OllamaBot()
        self.bot._write_out = self.print_console_word
        self.running = True
        self.user_name = user_name
        self.bot_name = bot_name
        self.system_name = system_name
        self.fm_name = fm_name

    def print_console_word(self, word: str):
        print(word, end='', flush=True)
        self.bot_msg = self.bot_msg + word

    def new_dialog(self):
        self.bot.new_chat()
        clear_console()
        print('User clear,stack was cleared. New chat will begin.')
        greet()

    def chat(self, msg):
        msg = msg.strip()
        print(Fore.CYAN + self.bot_name + ': ', end='')
        self.bot.chat(msg)
        # self.util.chat(msg, context=self.msg_stack)
        print(Style.RESET_ALL)

    def loop(self):
        self.bot_msg = ''
        print(Fore.LIGHTGREEN_EX + self.user_name + ': ', end='')
        msg = input()
        print(Style.RESET_ALL, end='')
        if not msg:
            return
        if is_quit(msg):
            self.running = False
            return
        if os.path.exists(msg):
            msg = f'file:{msg}'
        ai, dialog = process_ai_message(msg)
        if ai:
            out_ai_role_msg(self.fm_name, self.system_name, msg, dialog)
        else:
            self.chat(msg)
            try:
                term_width = int(os.get_terminal_size().columns / 3)
            except:
                term_width = 100
            tips_out(' - ' * term_width)
