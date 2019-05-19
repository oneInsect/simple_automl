
import pandas as pd


def task_executor(task_info):
    """Execute task
    :param task_info: detail of task, dict"""
    data_path = task_info.get("data_path")
    data_set = pd.read_csv(data_path)
