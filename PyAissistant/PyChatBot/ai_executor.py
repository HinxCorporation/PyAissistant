import logging

from .. import ai_assist


class AIExecutor:
    def __init__(self):
        self.tools = []
        self.functions = []

    def clear_tools(self):
        self.tools = []
        self.functions = []

    # def remove_tool(self, tool):
    #     self.functions.remove(tool)
    #     self.tools.remove(ai_assist.collect_function_as_tool(tool))

    def add_tool(self, tool):
        self.functions.append(tool)
        self.tools.append(ai_assist.collect_function_as_tool(tool))

    def extend(self, tools):
        self.extend_tools(tools)

    def extend_tools(self, tools):
        for tool in tools:
            self.add_tool(tool)

    def _get_local_functions_by_name(self, method_name):
        for func in self.functions:
            if func.__name__ == method_name:
                return func
        return None

    def list_tools(self):
        functions_names = [func.__name__ for func in self.functions]
        return functions_names

    def execute(self, function_tool, **kwargs):
        tool_details = function_tool['function']
        function_name = tool_details['name']
        function_desc = tool_details['description']
        logging.info(f" - (ai) Executing function: {function_name} with args: {kwargs} , go for {function_desc}")
        matched_func = self._get_local_functions_by_name(function_name)
        if matched_func is not None:
            exec_result = matched_func(**kwargs)
            if exec_result is not None:
                logging.info(f" - (ai) Function {function_name} executed successfully, return value: {exec_result}")
                return exec_result
            else:
                logging.info(f" - (ai) Function {function_name} executed successfully, but no return value found.")
                return f"Function {function_name} successfully executed, but no return value found."
        else:
            logging.error(f" - (ai) Function not found: {function_name}")
            return None
