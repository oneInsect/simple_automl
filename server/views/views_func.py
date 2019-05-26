import time
import pandas as pd
from autosklearn.classification import AutoSklearnClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ..apps import LOG, ServerException
from ..models import Task


def task_executor(task_info):
    """Execute task
    :param task_info: detail of task, dict"""
    data_path = task_info.get("data_path")
    time_max = task_info.get("time_max")
    task_id = task_info.get("task_id")
    LOG.info("Load data, path=%s", data_path)
    status = "done"
    try:
        data_set = pd.read_csv(data_path)
        x_set = data_set[data_set.columns[:len(data_set.keys()) - 1]]
        y_set = data_set[data_set.columns[-1]]
        x_train, x_test, y_train, y_test = train_test_split(
            x_set, y_set, test_size=0.3, random_state=0)
        LOG.info("start optimizer.")
        model = AutoSklearnClassifier(
            time_left_for_this_task=time_max + 5,
            per_run_time_limit=int(time_max/10),
            include_preprocessors=["no_preprocessing"],
        )
        model.fit(x_train, y_train)
        prediction = model.predict(x_test)
        accuracy = accuracy_score(y_test, prediction)
    except ServerException as server_error:
        LOG.error("Some thing wrong, reason=%s", server_error)
        accuracy = 0
        status = "failed"
    LOG.info("The accuracy is %s", accuracy)
    update = dict(end_time=int(time.time()),
                  best_accuracy=accuracy,
                  status=status)
    Task.objects.filter(task_id=task_id).update(**update)

