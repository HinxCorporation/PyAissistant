import json


class DeepSeekMessageUnit:
    def __init__(self, role):
        self.role = role
        self.type = 'undefined'

    def is_function_call(self):
        return self.type == 'function'

    def is_message(self):
        return self.type == 'message'


class DeepSeekCall(DeepSeekMessageUnit):
    def __init__(self, call_id, call_type, call_function, call_func_arg):
        super().__init__('assistant')
        self.call_index = -1
        self.call_id = call_id
        self.call_type = call_type
        self.call_function = call_function
        self.call_func_arg = call_func_arg
        self.type = 'function'

    def function_call(self):
        return {
            "id": self.call_id,
            "type": self.call_type,
            "function": {
                "name": self.call_function,
                "arguments": self.call_func_arg
            }
        }

    def call_expression(self):
        return f"{self.call_function} : {self.call_func_arg} , -> {self.call_id}"
        # return (f"DeepSeekCall(call_id={self.call_id}, call_type={self.call_type}, call_function={
        # self.call_function}, " f"call_func_arg={self.call_func_arg})")

    def args_dict(self):
        return json.loads(self.call_func_arg.strip())

    def get_function_name(self):
        return self.call_function

    def get_function_call_id(self):
        return self.call_id


class DeepSeekMessageContent(DeepSeekMessageUnit):
    def __init__(self, content):
        super().__init__('assistant')
        self.content = content
        self.type = 'message'


class DeepSeekChoiceUnit:
    def __init__(self, index, logprobs, finish_reason):
        self.index = index
        self.message: DeepSeekMessageContent
        self.message = None
        self.tool_calls = []
        self.logprobs = logprobs
        self.finish_reason = finish_reason

    def get_call_by_index(self, index):
        for call in self.tool_calls:
            if call.call_index == index:
                return call
        return None

    def process_message(self, msg):
        if msg is None:
            return None
        # [{"role":"assistant","content":""}}]},
        # [{"tool_calls":[{"index":0,"id":"call__7bcf115b-c84e-4c4c-91de-a32f1e5cc3e","type":"function",
        # "function":{"name":"open_browser","arguments":""}}]}}]},
        # [{"tool_calls":[{"index":0,"function":{"arguments":"{\""}}]}}]},
        role = msg.get('role', '')
        content = msg.get('content', '')

        if self.message is None:
            self.message = DeepSeekMessageContent(content)
        else:
            self.message.content += content

        if role:
            self.message.role = role

        tool_calls = msg.get('tool_calls', None)
        if tool_calls is not None:
            for call in tool_calls:
                call_index = call.get('index', 0)
                call_unit = self.get_call_by_index(call_index)

                call_function = call.get('function', '')
                call_func_arg = call_function.get('arguments', '')
                if call_unit is None:
                    call_id = call.get('id', '')
                    call_type = call.get('type', '')
                    call_function_name = call_function.get('name', '')
                    call_unit = DeepSeekCall(call_id, call_type, call_function_name, call_func_arg)
                    call_unit.call_index = call_index
                    self.tool_calls.append(call_unit)
                else:
                    call_unit.call_func_arg += call_func_arg
        return content


class DeepSeekResponse:
    def __init__(self, response_id, object_type, created, model, choices, usage, system_fingerprint):
        self.response_id = response_id
        self.object_type = object_type
        self.created = created
        self.model = model
        self.choices = choices
        self.usage = usage
        self.system_fingerprint = system_fingerprint

    def get_choice_by_index(self, index):
        for choice in self.choices:
            if choice.index == index:
                return choice
        return None

    def get_functions_calls(self):
        return [call.tool_calls for call in self.choices]

    def processes_choices(self, choices):
        words = None
        for choice in choices:
            index = choice.get('index')
            if index is None:
                continue
            choice_unit = self.get_choice_by_index(index)
            if choice_unit is None:
                choice_unit = DeepSeekChoiceUnit(index, None, None)
                self.choices.append(choice_unit)

            message = choice.get('delta', "")
            if not message:
                message = choice.get('message', '')
            words = choice_unit.process_message(message)
            logprobs = choice.get('logprobs', None)
            if logprobs is not None:
                choice_unit.logprobs = logprobs

            finish_reason = choice.get('finish_reason', None)
            if finish_reason is not None:
                choice_unit.finish_reason = finish_reason
        return words


class DeepSeekMessage:

    def __init__(self):
        self.chain = []

    def find_block_on_chain_by_id(self, block_id):
        for block in self.chain:
            if block.response_id == block_id:
                return block
        return None

    def get_extras(self):
        stacks = [response.get_functions_calls() for response in self.chain]
        functions = []
        for stack in stacks:
            for items in stack:
                functions.extend(items)
        return functions

    def process_new_line(self, line):
        line = line.strip()
        if not line:
            return None
        if not line.startswith('{'):
            return None
        if not line.endswith('}'):
            return None

        response = json.loads(line)
        response_id = response.get('id', '')
        block = self.find_block_on_chain_by_id(response_id)
        if block is None:
            object_type = response.get('object', '')
            created = response.get('created', '')
            model = response.get('model', '')
            block = DeepSeekResponse(response_id, object_type, created, model,
                                     [], {}, '')
            self.chain.append(block)

        choices = response.get('choices')
        words = None
        if choices is not None:
            words = block.processes_choices(choices)

        if block.usage is None:
            usage = response.get('usage', '')
            if usage:
                block.usage = usage

        if not block.system_fingerprint:
            system_fingerprint = response.get('system_fingerprint', '')
            if system_fingerprint:
                block.system_fingerprint = system_fingerprint

        if words:
            return words
        else:
            return None
