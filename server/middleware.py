import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from .apps import LOG


class GlobalException(MiddlewareMixin):

    def process_exception(self, _, exception):
        LOG.error(str(exception))
        return HttpResponse(content=json.dumps({"msg": str(exception)}),
                            status=500)
