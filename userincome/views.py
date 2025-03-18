import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from userincome.models import Source, UserIncome
from userpreferences.models import UserPreferences


# Create your views here.
@csrf_exempt
def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        sources = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user
        ) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user
        ) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user
        ) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user
        )

        data =sources.values()
        return JsonResponse(list(data), safe=False)




@login_required(login_url="authentication/login")
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency =UserPreferences.objects.get(user=request.user).currency
    context = {
        "source": source,
        "income": income,
        "page_obj": page_obj,
        "currency": currency,

    }
    return render(request, "income/index.html", context)


def add_income(request):
    sources = Source.objects.all()
    context = {"sources": sources, "values": request.POST}

    if request.method == "GET":

        return render(request, "income/add_income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Please enter your amount")
            return render(request, "income/add_income.html", context)
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not description:
            messages.error(request, "Please enter your description")
            return render(request, "income/add_income.html", context)
        if not date:
            messages.error(request, "Please select a date")
            return render(request, "income/add_income.html", context)
        if not source:
            messages.error(request, "Please select a source")
            return render(request, "income/add_income.html", context)
        UserIncome.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date,
        )
        messages.success(request, "Income Added")
        return redirect("income")
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    values = {
        "amount": income.amount,
        "description": income.description,
        "income_date": income.date.strftime("%Y-%m-%d") if income.date else "",
        "source": income.source
    }
    context = {"income": income,
               "values": values,
               "source": source,
               }

    if request.method == "GET":
        return render(request, "income/income_edit.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
    if not amount:
        messages.error(request, "Please enter your amount")
        return render(request, "income/income_edit.html", context)
    description = request.POST.get("description")
    date = request.POST.get("income_date")
    source = request.POST.get("source")
    if not description:
        messages.error(request, "Please enter your description")
        return render(request, "income/income_edit.html", context)
    if not date:
        messages.error(request, "Please select a date")
        return render(request, "income/income_edit.html", context)

    income.owner = request.user
    income.amount = amount
    income.description = description
    income.source = source
    income.date = date
    income.save()
    messages.success(request, "Income updated successfully")
    return redirect("income")

def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income deleted successfully")
    return redirect("income")
