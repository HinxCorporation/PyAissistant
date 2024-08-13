import json

__collected_exposed_functions__ = []


def ai_exposed_function(func):
    """将方法暴露给AI"""
    __collected_exposed_functions__.append(func)
    return func


def list_exposed_functions() -> []:
    """
    列出所有暴露给AI的函数
    :return: 所有暴露给AI的函数列表
    """
    return __collected_exposed_functions__


def collect_display_info(func):
    func_name = func.__name__
    func_doc = func.__doc__
    return {"name": func_name, "doc": func_doc}


@ai_exposed_function
def list_all_functions() -> str:
    """
    列出所有可用的函数
    :return: json: 所有可用的函数列表
    """
    my_list = [collect_display_info(func) for func in __collected_exposed_functions__]
    return json.dumps(my_list)
