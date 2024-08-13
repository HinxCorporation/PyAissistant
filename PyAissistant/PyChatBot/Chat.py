from datetime import datetime


class Message:
    """基础类型的信息"""
    def __init__(self, content: str, user='user', sid='0', title=''):
        self.role = user
        self.content = content
        self.id = sid
        self.title = title
        self.time = datetime.now()

    @property
    def message_dict(self):
        return {
            'role': self.role,
            'content': self.content,
        }


class ToolCallMessage(Message):
    """
    工具调用信息，包含多个工具调用，每个工具调用包含一个id，函数名，参数，返回值
    """
    def __init__(self, tool_calls, content: str = "", role: str = "assistant", call_id: str = ""):
        super().__init__(content, role, call_id, title='tool_call')
        self.functions = tool_calls

    @property
    def message_dict(self):
        return {
            'role': self.role,
            'content': self.content,
            'tool_calls': [call.function_call() for call in self.functions]
        }


class ToolResponse(Message):
    """
    工具响应信息，包含一个工具调用的id，函数名，参数，返回值
    """
    def __init__(self, content: str, tool_id: str, ):
        super().__init__(content, 'tool', tool_id, title='tool_response')
        self.tool_id = tool_id

    @property
    def message_dict(self):
        return {
            'role': "tool",
            'content': self.content,
            'tool_call_id': self.tool_id,
        }


class Chat:
    def __init__(self):
        self.messages = []
        self.id = 0
        # time is now
        self.time = datetime.now()
        self.title = 'new chat'
        self.model = "model"
        self.system_prompt = "you are a good assistant"
        self.context = ''


class ToolCall:
    """
    each call has it own call id , function name, args, and response
    """

    def __init__(self, calls: list, role: str, id: str):
        self.role = role
        self.calls = calls
        self.id = id
        self.time = datetime.now()

    def process_calling(self):
        stack_data = []
        for call in self.calls:
            if call['type'] == 'function':
                call_id = call['id']
                function_name = call['function']['name']
                function_args = call['function']['arguments']
                # call the function with arguments
                response = function_name(**function_args)
                stack_data.append({'id': call_id, 'response': response, "caller": self.role})

        return stack_data

    def get_schema(self):
        schema = {}
        for call in self.calls:
            if call['type'] == 'function':
                function_name = call['function']['name']
                function_args = call['function']['arguments']
                # get the schema of the function
                schema[function_name] = function_args

        return schema
