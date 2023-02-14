from django.db import models

# Create your models here.
class ScrapeTask(models.Model):
    task_id = models.CharField(max_length=36)
    search = models.CharField(max_length=36)
    # status  = models.CharField(default="INITIATED")
    # csv_file = models.CharField(max_length=50000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.search