from django.apps import AppConfig
import os


class ServerConfig(AppConfig):
    name = 'server'


APP_DIR = os.path.dirname(os.path.abspath(__file__))
