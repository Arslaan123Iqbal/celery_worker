from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerytask.settings')

app = Celery('celerytask')

app.conf.enable_utcv = False

app.conf.update(timezone = 'Asia/Karachi')

app.config_from_object(settings, namespace="CELERY")

# Celery beat Setting
app.conf.beat_schedule = {
    
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


