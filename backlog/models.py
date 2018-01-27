from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class BackLog(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey(User, related_name='backlogs', on_delete=models.DO_NOTHING, null=True, blank=True)
    start_at = models.DateField(auto_now=True)
    end_at = models.DateField(auto_now_add=False, auto_now=False, null=True)

    def __str__(self):
        return self.name


class Sprint(models.Model):
    name = models.CharField(max_length=25)
    start_at = models.DateField(auto_now_add=True)
    end_at = models.DateField(auto_now_add=False, auto_now=False, null=True)
    is_done = models.BooleanField(default=False)
    backlog = models.ForeignKey(BackLog, related_name='sprints', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    importance = models.IntegerField()
    status = models.IntegerField(default=1)  # 1: Not started   2: In Progress   3: Done
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    start_at = models.DateField(auto_now_add=True)
    end_at = models.DateField(auto_now_add=False, auto_now=False)
    assigned_user = models.ForeignKey(User, related_name='tasks', on_delete=models.DO_NOTHING)
    sprint = models.ForeignKey(Sprint, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
