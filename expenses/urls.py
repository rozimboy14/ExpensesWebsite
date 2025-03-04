from django.urls import path
from .views import index,add_expense

urlpatterns = [
    path('', index, name='expenses'),
    path('add_expenses',add_expense, name='add_expenses'),
]