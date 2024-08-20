import inspect


class FunctionParameter:
    def __init__(self, param_type, description):
        self.type = param_type
        self.description = description


class FunctionProperties:
    def __init__(self):
        self.properties = {}

    def add_property(self, name, param):
        self.properties[name] = param.__dict__


class FunctionParameters:
    def __init__(self, param_type, properties, required, additionalProperties=False):
        self.type = param_type
        self.properties = properties
        self.required = required
        self.additionalProperties = additionalProperties


class Function:
    def __init__(self, name, description, parameters):
        self.name = name
        self.strict: False
        self.description = description
        self.parameters = parameters


class FunctionPayload:
    def __init__(self, payload_type, function):
        self.type = payload_type
        self.function = function.__dict__


def create_payload_from_function(func):
    """
    Create a payload object from a function
    :param func:
    :return:
    """
    # Extract function metadata
    func_name = func.__name__
    func_description = func.__doc__.strip() if func.__doc__ else "No description provided"

    # Extract function parameters
    sig = inspect.signature(func)
    properties = FunctionProperties()
    required = []

    for param_name, param in sig.parameters.items():
        if param.annotation == str:
            param_type = "string"
        else:
            param_type = "object"  # You can extend this to handle other types
        description = f"Description for {param_name}"  # This should be dynamically set based on your requirements
        param_obj = FunctionParameter(param_type, description)
        properties.add_property(param_name, param_obj)
        required.append(param_name)

    parameters = FunctionParameters("object", properties.properties, required)
    function = Function(func_name, func_description, parameters.__dict__)
    payload = FunctionPayload("function", function)

    return payload.__dict__
