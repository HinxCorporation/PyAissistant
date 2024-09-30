import requests

deepseek_api = 'https://api.deepseek.com'
"""deepseek api url"""

deepseek_api_openai_compatible = 'https://api.deepseek.com/v1'
"""deepseek openai compatible api url"""

deepseek_api_beta = 'https://api.deepseek.com/beta'
"""beta api url"""


def chat_completion(base_url):
    """chat completion url"""
    return base_url + '/chat/completion'


def fim_completion():
    """fill in middle completion url"""
    return deepseek_api_beta + '/completion'


def list_models():
    """list models url"""
    return deepseek_api + '/models'


def list_models_beta():
    """list models beta url"""
    return deepseek_api_beta + '/models'


def get_user_balance():
    """get user balance url"""
    return deepseek_api + '/user/balance'


class DeepSeekAPI:
    """
    API client for DeepSeek API.
    Get models, usage
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def create_request(self, url):
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        return requests.request("GET", url, headers=headers, data=payload,proxies={"http": "", "https": ""})

    @property
    def usage(self):
        return self.create_request(get_user_balance())

    @property
    def models(self):
        return self.create_request(list_models())
