def description():
    return ('The FIM (Fill-In-the-Middle) Completion API. User must set base_url="https://api.deepseek.com/beta" to '
            'use this feature.')


class Request:
    """
    The FIM (Fill-In-the-Middle) Completion API ( Request Body).
    User must set base_url="https://api.deepseek.com/beta" to use this feature.
    """
    model: str
    prompt: str
    echo: bool
    frequency_penalty: float
    logprobs: int
    max_tokens: int
    presence_penalty: float
    stop: object
    stream: bool
    stream_options: object
    suffix: str
    temperature: float
    top_p: float


def demo(key):

    print('\033[36m------------------ FIM (Fill-In-the-Middle) Completion Demo ------------------------\033[0m')
    from openai import OpenAI
    # user should set `base_url="https://api.deepseek.com/beta"` to use this feature.
    client = OpenAI(
        api_key=key,
        base_url="https://api.deepseek.com/beta",
    )
    response = client.completions.create(
        model="deepseek-chat",
        prompt="def fib(a):",
        suffix="    return fib(a-1) + fib(a-2)",
        max_tokens=128)
    print(response.choices[0].text)


def demo_rest(key):
    import requests
    import json
    print('\033[36m------------------ FIM (Fill-In-the-Middle) Completion Demo REST API ------------------------\033[0m')
    url = "https://api.deepseek.com/beta/completions"

    payload = json.dumps({
        "model": "deepseek-chat",
        "prompt": "Once upon a time, ",
        "echo": False,
        "frequency_penalty": 0,
        "logprobs": 0,
        "max_tokens": 1024,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "stream_options": None,
        "suffix": None,
        "temperature": 1,
        "top_p": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {key}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
