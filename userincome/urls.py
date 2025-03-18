from django.urls import path

from django.views.generic import detail

from .views import index, add_income, edit_income, delete_income, search_income

urlpatterns = [
    path('', index, name='income'),
    path('add_income',add_income, name='add_income'),
    path('edit_income/<int:id>', edit_income, name='income_edit'),
    path('delete_income/<int:id>', delete_income, name='income_delete'),
    path('search_income', search_income, name='search_income'),

]