import json

from openai import OpenAI


def demo_function_call(key):
    """
    Function Calling allows the model to call external tools to enhance its capabilities.

    Sample Code
    Here is an example of using Function Calling to get the current weather information of the user's location,
    demonstrated with complete Python code.

    For the specific API format of Function Calling, please refer to the Chat Completion documentation.
    :param key:
    :return:
    """
    print('\033[36m------------------ Function Calling Demo ------------------------\033[0m')

    def send_messages(user_msgs):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=user_msgs,
            tools=tools
        )
        return response.choices[0].message

    client = OpenAI(
        api_key=key,
        base_url="https://api.deepseek.com",
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather of an location, the user shoud supply a location first",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"]
                },
            }
        },
    ]

    messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
    message = send_messages(messages)
    print(f"User>\t {messages[0]['content']}")

    tool = message.tool_calls[0]
    messages.append(message)

    messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
    message = send_messages(messages)
    print(f"Model>\t {message.content}")


def demo_json_output(key):
    """
    In many scenarios, users need the model to output in strict JSON format to achieve structured output, facilitating subsequent parsing.

    DeepSeek provides JSON Output to ensure the model outputs valid JSON strings.

    Notice
    To enable JSON Output, users should:

    Set the response_format parameter to {'type': 'json_object'}.
    Include the word "json" in the system or user prompt, and provide an example of the desired JSON format to guide the model in outputting valid JSON.
    Set the max_tokens parameter reasonably to prevent the JSON string from being truncated midway.
    :param key:
    :return:
    """
    print('\033[36m------------------ JSON Output Demo ------------------------\033[0m')
    client = OpenAI(
        api_key=key,
        base_url="https://api.deepseek.com",
    )

    system_prompt = """
    The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

    EXAMPLE INPUT: 
    Which is the highest mountain in the world? Mount Everest.

    EXAMPLE JSON OUTPUT:
    {
        "question": "Which is the highest mountain in the world?",
        "answer": "Mount Everest"
    }
    """

    user_prompt = "Which is the longest river in the world? The Nile River."

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    print(json.loads(response.choices[0].message.content))
