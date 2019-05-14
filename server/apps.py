from django.apps import AppConfig
import os
import logging


class ServerConfig(AppConfig):
    name = 'server'


def init_log(log_dir, service_name):
    """init logger object.
    :param log_dir: dir of logfile,str
    :param service_name: name of logfile.str
    :return logger: logger object."""
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    log_dir = os.path.join(log_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # create handler output to file
    handler = logging.FileHandler(
        os.path.join(log_dir, service_name+'.log'), mode='a')
    handler.setLevel(logging.INFO)

    # handler output to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(ch)
    return logger


APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = init_log(APP_DIR, ServerConfig.name)
