"""simple_automl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from server.views import index_views, preview_views, trial_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # download sample data set
    path('api/v1/automl/dataset/<str:file_name>', index_views.download_dataset),
    # return version info
    path('api/v1/automl/version', index_views.version),
    # Get: Get all tasks preview
    # Post: add a new task
    path('api/v1/automl/task', index_views.tasks),
    # Delete、get a task
    path('api/v1/automl/task/<str:task_id>', index_views.task),

    # start a task
    path('api/v1/automl/task/<str:task_id>/start', preview_views.start),
    # Get: task status
    path('api/v1/automl/task/status/<str:task_id>', preview_views.status),

    # Get: get trial by task_id
    path('api/v1/automl/trial/<str:task_id>', trial_views.trials),
]
