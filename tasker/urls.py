from django.contrib import admin
from django.urls import path,include
from .views import test,sendingmail

urlpatterns = [
    path('',test, name="test"),
    path('mail/',sendingmail, name="test")
]
