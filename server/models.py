import time
from django.db import models

# Create your models here.


class Task(models.Model):
    """Task model."""
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100, unique=True)
    create_time = models.IntegerField(default=int(time.time()))
    start_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)
    data_path = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="ready")
    model_name = models.CharField(max_length=100)
    hyper_parameters = models.TextField()

    def __str__(self):
        return u'%s %s' % (self.task_id, self.task_name)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'task_info'


class Trial(models.Model):
    """trial model"""
    task_id = models.IntegerField()
    trial_id = models.AutoField(primary_key=True)
    start_time = models.IntegerField(default=int(time.time()))
    end_time = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    hyper_parameters = models.TextField()

    def __str__(self):
        return u'%s %s' % (self.task_id, self.trial_id)

    class Meta:
        verbose_name = 'trial'
        verbose_name_plural = 'trial_info'
