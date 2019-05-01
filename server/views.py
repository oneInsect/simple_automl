from django.http import HttpResponse
# Create your views here.


def version(_):
    """Get software version.
    :return str: 'V 1.0.0'"""
    return HttpResponse("V 1.0.0")


