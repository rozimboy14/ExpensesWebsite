from django.shortcuts import render
from django.views import View


def index(request):
     return  render(request ,'expenses/index.html',)
def add_expense(request):
    return render(request,'expenses/add_expenses.html')