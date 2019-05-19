
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Task


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
