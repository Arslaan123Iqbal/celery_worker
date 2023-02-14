from django.contrib import admin
from django.urls import path,include
from .views import test, scrape_view, test2,task_status,getData

urlpatterns = [
    path('',test, name="test"),
    # path('mail/',sendingmail, name="test"),
    path('scrape/',scrape_view, name="test"),
    path('test/<str:search>',test2, name="test2"),
    path('status/<str:task_id>',task_status, name="status"),
    path('status',getData, name="statusus"),
]
