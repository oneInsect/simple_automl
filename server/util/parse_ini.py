"""
CreateTime    : 2019/5/19 16:36
Author        : X
Filename      : parse_ini.py
"""
import os
from configparser import ConfigParser
from ..apps import APP_DIR


def parse_ini(conf_name, section=None, option=None):
    """Parse ini config file
    :param conf_name: config file name, str
    :param section: section of config, str
    :param option: option of config, str
    """
    conf_path = os.path.join(APP_DIR, "etc", conf_name)
    parse = ConfigParser().read(conf_path)
    return parse.get(section, option)
