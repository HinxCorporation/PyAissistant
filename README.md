# PyAissistant

<p align="center">

[![PyPI Version](https://img.shields.io/pypi/v/pyaissistant.svg)](https://pypi.org/project/pyaissistant/)[![PyPI Downloads](https://img.shields.io/pypi/dm/pyaissistant.svg)](https://pypi.org/project/pyaissistant/)

</p>

Welcome to **Py AI Assistant**, a Python package designed to provide a user-friendly interface for AI developers working with Python. This package aims to streamline the integration of AI functionalities into your projects, making it easier to leverage advanced AI capabilities.

- A user-friendly interface for AI developers working with Python.
- Streamline the integration of AI functionalities into your projects.
- Leverage advanced AI capabilities.

## Features

- **AI Chat Completion**: Engage in interactive conversations with AI models.
- **AI Tool Call**: Utilize AI-powered tools for various tasks.
- **AI Region Support**:
  - **DeepSeek AI**: Dive deep into AI research and development.
  - **Ollama Local Run API**: Work with local AI models seamlessly.

## Installation

To install the `PyAissistant` package, you can use pip:

```bash
pip install PyAissistant
```

As for update this package, you can use:

```bash
pip install --upgrade PyAissistant
```

## Usage

show hello from the package and learn from the tips

```python
from PyAissistant import hello

# show hello from PyAissistant
hello()
```

create a first console chat demo

```python
from PyAissistant import *
from PyAissistant.PyChatBot.chat_api import ChatBot
from PyAissistant.PyChatBot.deep_seek_bot import DeepSeekBot

def read_message():
    return input("\nYou: ")

def ai_chat_example(dialogs=2):
    init_coder()
    list_all_functions()

    bot: ChatBot = DeepSeekBot()
    while dialogs > 0:
        message = read_message()
        bot.chat(message)
        dialogs -= 1

if __name__ == '__main__':
    # run a demo of chatbot
    ai_chat_example()
    print()
    print("Done! Bye")
```

Let AI tells you what it can do

```python
def list_all_functions():
    bot: ChatBot = DeepSeekBot()
    bot.chat('Hi bot, list all functions please.')
```

more in coming

## Documentation

For more detailed information on how to use the `PyAissistant` package, please refer to the [official documentation](https://PyAissistant.readthedocs.io).

## Contributing

We welcome contributions from the community! If you're interested in contributing to `PyAissistant`, please check out our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support

If you encounter any issues or have any questions, please open an issue on our [GitHub repository](https://github.com/HinxCorporation/PyAissistant).

---

Thank you for using `PyAissistant`! We hope this package helps you in your AI development journey.
