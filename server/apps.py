from django.apps import AppConfig
import os
from .util import get_logger, setup_logger


APP_DIR = os.path.dirname(os.path.abspath(__file__))


class ServerConfig(AppConfig):
    name = 'server'


setup_logger(output_file=os.path.join(APP_DIR, 'logs', 'server.log'))
LOG = get_logger("server")
