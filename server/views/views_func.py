import time
import pandas as pd
import platform
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from ..apps import LOG, ServerException
from ..models import Task


def task_executor(task_info):
    """Execute task
    :param task_info: detail of task, dict"""
    data_path = task_info.get("data_path")
    time_max = task_info.get("time_max")
    task_id = task_info.get("task_id")
    model_type = task_info.get("model_type")
    LOG.info("Load data, path=%s", data_path)
    status = "done"
    try:
        data_set = pd.read_csv(data_path)
        x_set = data_set[data_set.columns[:len(data_set.keys()) - 1]]
        y_set = data_set[data_set.columns[-1]]
        x_train, x_test, y_train, y_test = train_test_split(
            x_set, y_set, test_size=0.3, random_state=0)
        LOG.info("start optimizer.")
        if platform.system() == "Linux":
            from autosklearn.classification import AutoSklearnClassifier
            from autosklearn.regression import AutoSklearnRegressor
            if model_type == "Classification":
                model = AutoSklearnClassifier(
                    time_left_for_this_task=time_max + 5,
                    per_run_time_limit=int(time_max/10),
                    include_preprocessors=["no_preprocessing"],
                )
            elif model_type == "Regression":
                model = AutoSklearnRegressor(
                    time_left_for_this_task=time_max + 5,
                    per_run_time_limit=int(time_max/10),
                    include_preprocessors=["no_preprocessing"],
                )
            else:
                LOG.error("not support model type=%s", model_type)
                raise ValueError("not support model type")
        else:
            from sklearn.ensemble import RandomForestClassifier, \
                RandomForestRegressor
            if model_type == "Classification":
                model = RandomForestClassifier(n_estimators=500)
            elif model_type == "Regression":
                model = RandomForestRegressor(n_estimators=500)
            else:
                LOG.error("not support model type=%s", model_type)
                raise ValueError("not support model type")
        model.fit(x_train, y_train)
        prediction = model.predict(x_test)

        if model_type == "Classification":
            best_metrics = accuracy_score(y_test, prediction)
            LOG.info("The accuracy is %s", best_metrics)
        else:
            best_metrics = mean_squared_error(y_test, prediction)
            LOG.info("The mse is %s", best_metrics)
    except ServerException as server_error:
        LOG.error("Some thing wrong, reason=%s", server_error)
        best_metrics = 0
        status = "failed"

    update = dict(end_time=int(time.time()),
                  best_metrics=best_metrics,
                  status=status)
    Task.objects.filter(task_id=task_id).update(**update)

