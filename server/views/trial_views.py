
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models import Task, Trial
from ..apps import APP_DIR


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
