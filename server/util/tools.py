"""
CreateTime    : 2019/6/4 22:26
Author        : X
Filename      : tools.py
"""
import os
import json
from ..apps import APP_DIR


def load_config(file_name):
    """
    Load json config file.
    :param file_name: str, the name of config file
    :return: json
    """
    file_path = os.path.join(APP_DIR, "etc", file_name)
    with open(file_path) as config:
        return json.load(config)