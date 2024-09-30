from typing import Iterable


class Request:
    """
    The Request body of the chat completion API.
    """
    messages: []  # required
    model: str  # required
    frequency_penalty: float = 0.0  # -2 < v < 2
    max_tokens: int = 1000  # >1
    presence_penalty: float = 0.0  # -2 < v < 2
    response_format: object
    '''
    { "type": "json_object" } in text or json format
    An object specifying the format that the model must output. Setting to { "type": "json_object" } enables JSON 
    Output, which guarantees the message the model generates is valid JSON.
    '''
    stop: object
    """
    (string or string array) nullable Up to 16 sequences where the API will stop generating further
    """
    # tokens.
    stream: bool
    stream_options: object
    temperature: float = 1.0  # 0.0 < v < 2.0
    stop_p: float  # <=1.0
    tools: Iterable[dict]  #
    tool_choice: str
    """
    in [none,auto,required,**] specifies  like if force  {"type": "function", "function": {"name": "my_function"}}
    """
    logprobs: bool
    top_logprobs: int  # <=20> , use while logprobs is true


def demo_prefix_completion(key):
    """
    Demo of prefix completion using deepseek-chat model.
    :param key:
    :return:
    """
    from openai import OpenAI
    print('\033[36m------------------ Prefix Completion Demo ------------------------\033[0m')
    client = OpenAI(
        api_key=key,
        base_url="https://api.deepseek.com/beta",
    )

    messages = [
        {"role": "user", "content": "Please write quick sort code"},
        {"role": "assistant", "content": "```python\n", "prefix": True}
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stop=["```"],
    )
    print(response.choices[0].message.content)
