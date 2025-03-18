from django.urls import path

from django.views.generic import detail

from .views import index, add_expense, edit_expense, delete_expense, search_expenses, expense_category_summary, \
    statsView, export_csv, export_excel, export_pdf

urlpatterns = [
    path("", index, name="expenses"),
    path("add_expenses", add_expense, name="add_expenses"),
    path("edit_expense/<int:id>", edit_expense, name="expense_edit"),
    path("delete_expense/<int:id>", delete_expense, name="expense_delete"),
    path("search_expenses", search_expenses, name="search_expenses"),
    path('expense_category_summary',expense_category_summary,name='expense_category_summary'),
    path('stats',statsView,name='stats'),
    path('export_csv',export_csv,name='export_csv'),
    path('export_excel',export_excel,name='export_excel'),
    path('export_pdf',export_pdf,name='export_pdf'),
]
