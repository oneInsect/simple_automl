from django.db import models

# Create your models here.


class Task(models.Model):
    """Task model."""
    task_id = models.AutoField(primary_key=True)
    create_time = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    data_path = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    model_names = models.CharField(max_length=100, choices=(('0', 'RandomForest'),))
    hyper_parameters = models.TextField()


class Trial(models.Model):
    """trial model"""
    task_id = models.IntegerField()
    trial_id = models.AutoField(primary_key=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    status = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    hyper_parameters = models.TextField()
