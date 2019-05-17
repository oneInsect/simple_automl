
import os
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models import Task, Trial
from ..apps import APP_DIR


@require_http_methods(['GET'])
def get_data_set(_, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param _: nil.
        :return data_set: the preview of data set, dict
    """
    task_info = Task.objects.filter(task_id=task_id).values().get()
    data_set_path = task_info.get('data_path')
    if not os.path.exists(data_set_path):
        return HttpResponse("data set file is not exists.", status=500)
    data_set = pd.read_csv(data_set_path, nrows=5)
    data_set_json = data_set.to_json()
    return HttpResponse(data_set_json)


@require_http_methods(['GET'])
def start(_, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param _: nil.
        :return task_info: the detail of task, dict
    """
    task_info = Task.objects.filter(task_id=task_id).values().get()
    print(task_info)
    return JsonResponse({"status": "success"})
