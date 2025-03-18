from django.urls import path
from tkinter.font import names

from .views import index

urlpatterns = [
    path('', index,name="preferences"),
]