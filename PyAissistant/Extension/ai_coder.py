import json

from .ai_code_tool import *
from .ai_extension import ai_exposed_function as exposed_function

Workspace = 'ai_works_space'


@exposed_function
def ls(path: str):
    """
    list path, top level.
    :param path: the folder you want to list
    :return:result or top level files and folders, format json str
    """
    global Workspace
    location = os.path.join(Workspace, path)
    if not os.path.exists(location):
        return 'path not exist'
    sets = [json.dumps({
        "path": entry.path,
        "name": entry.name,
        "folder": entry.is_dir()
    }) for entry in os.scandir(location)]
    return '\n'.join(sets)


@exposed_function
def write_string(project, file_path, content, encoding='utf-8', mode='w'):
    """
    This function is used to write a string to a file.
    :param mode: write mode, default is 'w' or using for append mode, use 'a'
    :param encoding:  the encoding of the file, default is 'utf-8'
    :param project: the project of  file should be
    :param file_path: the relative path of the file, under the project folder
    :param content: the string content or text to be written to the file
    :return: result of writing the string to the file
    """
    try:
        full_path = os.path.join(Workspace, project, file_path)
        folder, pure_file_name = os.path.split(full_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(full_path, mode, encoding=encoding) as f:
            f.write(content)
        return 'success'
    except Exception as e:
        return str(e)


@exposed_function
def create_project_view_by_view_string(project, view_string):
    """
    This function is used to create a project view by view string.
    :param project: the project of the view should be
    :param view_string: the view string to be created , example of view string:
        ollama_api/
        ├── ollama_api/
        │   ├── __init__.py
        ├── setup.py
    tree_patterns = "├── ", "└── ", "│   " , each of them represent a next level of parent folder
    :return: result of creating the view
    """
    try:
        # root_path = os.path.join(Workspace, project)
        root_path = os.path.abspath(Workspace)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        create_files_from_text(root_path, view_string)
        return 'success'
    except Exception as e:
        return str(e)


def init_coder(ws: str = ""):
    if not ws:
        ws = 'ai_works_space'
    global Workspace
    Workspace = ws
