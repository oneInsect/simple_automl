from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class GlobalException(MiddlewareMixin):

    def process_exception(self, _, exception):
        print(exception)
        return HttpResponse(content=exception, status=500)
