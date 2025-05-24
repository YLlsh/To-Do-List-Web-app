from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task = models.TextField(default=None)
    due = models.DateField(null=True, blank=True)
    priority = models.CharField(default=None, max_length=20,blank=True)
    complete =models.BooleanField(default=False)
    def __str__(self):
        return f" {self.task} -- {self.due}  -- {self.priority}"

