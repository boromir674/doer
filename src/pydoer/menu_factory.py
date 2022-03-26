import configparser
import os
import json
from typing import Iterable, Union

from .menu_config import MenuConfig
from .task_design_factory import TaskDesignFactory


MY_DIR = os.path.dirname(os.path.realpath(__file__))


class MenuFactory:

    @classmethod
    def create(cls, *args, **kwargs):
        if type(args[0]) == str:
            task_files = [os.path.join(args[0], 'options', x) for x in os.listdir(os.path.join(args[0], 'options'))]
            master_file = os.path.join(args[0], 'menu.json')
            if not os.path.exists(master_file):
                master_file = None
        else:
            task_files = args[0]
            master_file = kwargs.get('master_file')
        return cls._create(task_files, master_file=master_file)

    @classmethod
    def _create(cls, task_files: Iterable[str], master_file: Union[str, None]=None):
        task_designs = [TaskDesignFactory.from_json_file(x) for x in task_files]
        config = configparser.ConfigParser()
        config.read(os.path.join(MY_DIR, 'defaults.cfg'))
        data = {
            'title': config['menu_design']['title'],
            'subtitle': config['menu_design']['subtitle'],
            'tasks': task_designs
        }
        if master_file:
            try:
                with open(master_file, 'r') as _master_file:
                    master_data = json.load(_master_file)
                    data.update(master_data)
            except Exception as error:
                raise error
        menu = MenuConfig.from_dict(data)
        return menu
