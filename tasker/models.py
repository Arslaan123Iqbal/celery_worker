from django.db import models

# Create your models here.
class ScrapeTask(models.Model):
    task_id = models.CharField(max_length=36)
    search = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)