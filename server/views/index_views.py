
import os
import re
import uuid
import shutil
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models import Task
from ..apps import APP_DIR, LOG

PATH_COMP = re.compile("^[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?")


@require_http_methods(['GET'])
def version(_):
    """Get software version.
    :return str: 'V 1.0.0'"""
    return HttpResponse("V 1.0.1")


@require_http_methods(['GET'])
def download_dataset(_, file_name):
    """
    Download sample data set.
    :param _:
    :param file_name: the name of dataset.
    :return:
    """
    if "/" not in file_name and file_name.endswith(".csv"):
        sample_data_path = os.path.join(APP_DIR, "example_dataset", file_name)
        if os.path.isfile(sample_data_path):
            sample_data = open(sample_data_path, 'rb')
            response = FileResponse(sample_data)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"'\
                                              % file_name
            return response
    return HttpResponse("Some thing maybe wrong!", status=500)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def tasks(request):
    """GET:
           :return list: all tasks.
       POST:
           :param request: task info.
           :return bool: operation states.
           """
    # Get: Get all tasks preview
    # Post: create a new task
    if request.method == "GET":
        task_list = Task.objects.all().values_list(
            "task_id", "task_name", "model_type",
            "data_name", "status").values()
        return JsonResponse({"data": [_task for _task in task_list],
                             "msg": "",
                             "code": 200})
    else:
        task_info = request.POST.dict()
        if not task_info.get("time_max"):
            del task_info["time_max"]
        if not task_info.get("hyper_parameters"):
            task_info["hyper_parameters"] = "{}"
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
        LOG.info("add task success")
        return JsonResponse({"data": {"status": "success"},
                             "msg": "success",
                             "code": 201})


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
        return JsonResponse({"data": task_info,
                             "msg": "",
                             "code": 200})
    elif request.method == "DELETE":
        task_info = Task.objects.filter(task_id=task_id).values().get()
        Task.objects.filter(task_id=task_id).delete()
        data_path = task_info.get("data_path")
        path_name = os.path.basename(os.path.dirname(data_path))
        if PATH_COMP.search(path_name):
            shutil.rmtree(os.path.dirname(data_path))
            LOG.info("Delete task success. task_id=%s", task_id)
        else:
            LOG.error("Delete path error")
        return JsonResponse({"data": {"status": "success"},
                             "msg": "success",
                             "code": 200})
