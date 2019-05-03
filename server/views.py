
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Trial


@require_http_methods(['GET'])
def version(_):
    """Get software version.
    :return str: 'V 1.0.0'"""
    return HttpResponse("V 1.0.0")


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def tasks(request):
    """GET:
           :return list: all tasks.
       POST:
           :param request: task info.
           :return bool: operation states.
           """
    if request.method == "GET":
        task_list = Task.objects.all().values_list("task_id", "task_name")
        return JsonResponse([_task for _task in task_list], safe=False)
    else:
        task_info = json.loads(request.body)
        Task.objects.create(**task_info)
        return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def task(request, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param request: nil.
        :return task_info: the detail of task, dict
    PUT:
        :param task_id: the identify of task.
        :param request: the key-value of partial task which update needed.
        :return flag: update success or failure.
    DELETE:
        :param task_id: the identify of task.
        :param request: nil.
        :return flag: delete success or failure.
    """
    if request.method == "GET":
        task_info = Task.objects.filter(task_id=task_id).values().get()
        return JsonResponse(task_info)
    elif request.method == "PUT":
        value = json.loads(request.body)
        Task.objects.filter(task_id=task_id).update(**value)
        return JsonResponse({"status": "success"})
    else:
        Task.objects.filter(task_id=task_id).delete()
        return JsonResponse({"status": "success"})


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


@require_http_methods(['GET'])
def trials(_, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param _: nil.
        :return trial_list: trials under the task, list
    """
    trial_list = Trial.objects.filter(task_id=task_id).values()
    return JsonResponse([trial for trial in trial_list], safe=False)
