from .chat_completion import Request as ChatCompletionRequest, demo_prefix_completion
from .deepseek import DeepSeekAPI, deepseek_api, deepseek_api_openai_compatible as deepseek_api_openai, \
    deepseek_api_beta, chat_completion, fim_completion
from .deepseek_demo import demo_function_call, demo_json_output
from .fim_completion import Request as FimCompletionRequest, demo as demo_fim_completion, \
    demo_rest as demo_fim_completion_rest
import configparser
import os


def demo_deepseek_service():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file, encoding='utf-8')
        sk = config.get('deepseek', 'key')
    else:
        print("Config file not found, please input your DeepSeek API key ")
        sk = input("Please input your DeepSeek API key: ")
        config['deepseek'] = {'key': sk}
    client = DeepSeekAPI(sk)

    print('\033[36m------------------ Usage and Models ------------------------\033[0m')
    print(client.usage.text)
    print(client.models.text)
    # expose proxy for demo
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    demo_prefix_completion(sk)
    demo_fim_completion(sk)
    demo_fim_completion_rest(sk)
    demo_function_call(sk)
    demo_json_output(sk)
    print("\n\n\033[32m[Demo finished]\033[0m")


__all__ = [
    'DeepSeekAPI',
    'deepseek_api',
    'deepseek_api_openai',
    'deepseek_api_beta',
    'chat_completion',
    'fim_completion',
    'ChatCompletionRequest',
    'FimCompletionRequest',
    'demo_prefix_completion',
    'demo_fim_completion',
    'demo_fim_completion_rest',
    'demo_function_call',
    'demo_json_output',
    'demo_deepseek_service'
]
