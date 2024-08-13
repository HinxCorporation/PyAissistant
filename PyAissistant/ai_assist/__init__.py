from .ai_tools import create_payload_from_function


def collect_function_as_tool(function):
    """Collects a function as a tool and returns a payload for it"""
    return create_payload_from_function(function)


if __name__ == '__main__':
    def get_weather(location: str):
        """Get weather of a location, the user should supply a location first"""
        pass

    # Test
    payload = collect_function_as_tool(get_weather)
    print(payload)
