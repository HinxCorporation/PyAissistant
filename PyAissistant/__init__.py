from .Extension import ai_exposed_function, list_all_functions,init_coder
from .PyChatBot import Message, ToolCallMessage, ToolResponse, Chat, ToolCall, AIExecutor, ChatBot, HinxtonChatBot, \
    ConsoleChat, DeepSeekOpenAI, DeepSeekBot, DeepSeekMessageUnit, DeepSeekCall, DeepSeekMessageContent, \
    DeepSeekChoiceUnit, DeepSeekResponse, DeepSeekMessage, OllamaBot
from .ai_assist import collect_function_as_tool

__all__ = [
    'ai_exposed_function',
    'list_all_functions',
    'Message',
    'ToolCallMessage',
    'ToolResponse',
    'Chat',
    'ToolCall',
    'AIExecutor',
    'ChatBot',
    'HinxtonChatBot',
    'ConsoleChat',
    'DeepSeekOpenAI',
    'DeepSeekBot',
    'DeepSeekMessageUnit',
    'DeepSeekCall',
    'DeepSeekMessageContent',
    'DeepSeekChoiceUnit',
    'DeepSeekResponse',
    'DeepSeekMessage',
    'OllamaBot',
    'collect_function_as_tool',
    'init_coder'
]


def __get_config_example():
    return r"""
[ai]
current=deepseek

[deepseek]
key=your deepseek api key here
host=https://api.deepseek.com
url=https://api.deepseek.com/chat/completions
current=deepseek-chat
default=deepseek-chatd,deepseek-coder

[setting]
cache_transitions=false
use_proxy=false
proxy=http://127.0.0.1:7890
note_root=\path\to\Obsidian Vault
chat_folders=AI-Chat,Other-Chat-Folder

[Colors]
user_dialog=0
system_dialog=4
assistant_dialog=#7e38ff

[Console]
use_nerd_font=true

[NERD]
char_user:
char_system:
char_computer:
char_bot:ﮧ
char_folder:
char_file:
char_code:
char_music:
char_movie:
char_book:
char_image:
char_github:
char_terminal:
char_firefox:
char_python:
char_man=
char_woman=
char_git=
char_search=
char_avatar=
char_header=
char_cat=
"""


def hello():
    greet()


def greet():
    """welcome message"""
    print("Welcome to PyAissistant!")
    print("This is a chatbot assistant that can help you with your daily tasks.")
    print('----------------------------------------------------------------------------')
    print('You could crate a default config file if you are first time using this assistant. via call '
          'create_config_file() function.')
    print('----------------------------------------------------------------------------')
    print('if you are going to using deep seek bot , you should provide your deep seek api key in the config file.')
    print('if you are going to using chat console, you could config the nerd char custom in the config file.')
    print('if you are going to using openai-api,just config the proxy if you are blocked by api region limitation.')
    print('----------------------------------------------------------------------------')
    print('This is the config example file. You can modify it to fit your needs.')
    print('')
    print(__get_config_example())


def create_config_file():
    """crate the config file with example content"""
    with open('config.ini', 'w', encoding='utf-8') as f:
        f.write(__get_config_example())
