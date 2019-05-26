"""
CreateTime    : 2019/5/19 16:36
Author        : X
Filename      : parse_ini.py
"""
from configparser import ConfigParser


def parse_ini(conf_path, section=None, option=None):
    """Parse ini config file
    :param conf_path: config file path, str
    :param section: section of config, str
    :param option: option of config, str
    """
    parse = ConfigParser().read(conf_path)
    return parse.get(section, option)
