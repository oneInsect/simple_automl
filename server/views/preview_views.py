import time
from threading import Thread
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Task
from .views_func import task_executor
from functools import partial


@require_http_methods(['GET'])
def start(_, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param _: nil.
        :return execute_status: success
    """
    task_obj = Task.objects.filter(task_id=task_id)
    task_info = task_obj.values().get()
    executor = partial(task_executor, task_info=task_info)
    execute = Thread(target=executor)
    execute.setDaemon(True)
    execute.start()
    start_time = int(time.time())
    task_obj.update(**{"status": "running", "start_time": start_time})
    response_data = {"status": "success",
                     "start_time": start_time}
    return JsonResponse({"data": response_data,
                         "msg": "success",
                         "code": 200})


@require_http_methods(['GET'])
def status(_, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param _: nil.
        :return task_status: dict
    """
    task_info = Task.objects.filter(task_id=task_id).values().get()
    best_accuracy = task_info.get("best_accuracy")
    start_time = task_info.get("start_time")
    end_time = task_info.get("end_time")
    time_max = task_info.get("time_max")
    _status = task_info.get("status")
    now = int(time.time())
    if not start_time:
        process_time = 0
    elif not end_time:
        process_time = now - start_time
    else:
        process_time = end_time - start_time
    time_percentile = int(process_time / time_max * 100)
    task_status = dict(status=_status,
                       end_time=end_time,
                       time_percentile=time_percentile,
                       best_accuracy=best_accuracy or '--')
    return JsonResponse({"data": task_status,
                         "msg": "success",
                         "code": 200})
