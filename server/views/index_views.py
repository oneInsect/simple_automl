
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models import Task
from ..apps import APP_DIR


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
        task_list = Task.objects.all().values_list(
            "task_id", "task_name", "model_name",
            "data_name", "status").values()
        return JsonResponse([_task for _task in task_list], safe=False)
    else:
        task_info = request.POST.dict()
        upload_file = request.FILES.get('file')
        path_id = uuid.uuid4().urn.split(":")[2]
        file_dir = os.path.join(APP_DIR, "data", path_id)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = os.path.join(file_dir, upload_file.name)
        with open(file_path, "wb") as file_obj:
            for chunk in upload_file.chunks():
                file_obj.write(chunk)
        task_info["data_path"] = file_path
        task_info["data_name"] = upload_file.name
        Task.objects.create(**task_info)
        return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(['GET', 'DELETE'])
def task(request, task_id):
    """
    GET:
        :param task_id: the identify of task.
        :param request: nil.
        :return task_info: the detail of task, dict
    DELETE:
        :param task_id: the identify of task.
        :param request: nil.
        :return flag: delete success or failure.
    """
    if request.method == "GET":
        task_info = Task.objects.filter(task_id=task_id).values().get()
        return JsonResponse(task_info)
    else:
        Task.objects.filter(task_id=task_id).delete()
        return JsonResponse({"status": "success"})
