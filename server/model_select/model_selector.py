"""
CreateTime    : 2019/6/4 22:43
Author        : X
Filename      : model_selector.py
"""
import json
import random
from ..util import parse_ini


class ModelSelector(object):
    """
    Select model based on model type.
    """
    def __init__(self, model_type):
        self.model_type = model_type
        self.support_models = self.load_support_models()

    def load_support_models(self):
        """
        load support model list from config
        :return: list of models
        """
        support_models = parse_ini("simple_automl.ini",
                                   "model_select", self.model_type.lower())
        support_models = json.loads(support_models)
        return support_models

    def random_search(self):
        """
        Select model based random choice
        :return: model_name
        """
        return random.choice(self.support_models)