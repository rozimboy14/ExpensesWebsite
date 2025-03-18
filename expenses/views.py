import csv
import json
import datetime
import xlsxwriter
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from expenses.models import ExpenseCategory, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum




@csrf_exempt
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user
        ) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user
        ) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user
        ) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user
        )

        data =expenses.values()
        return JsonResponse(list(data), safe=False)






@login_required(login_url="authentication/login")
def index(request):
    category = ExpenseCategory.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency =UserPreferences.objects.get(user=request.user).currency
    context = {
        "category": category,
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": currency,

    }
    return render(request, "expenses/index.html", context)


def add_expense(request):
    categories = ExpenseCategory.objects.all()
    context = {"categories": categories, "values": request.POST}

    if request.method == "GET":

        return render(request, "expenses/add_expenses.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Please enter your amount")
            return render(request, "expenses/add_expenses.html", context)
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not description:
            messages.error(request, "Please enter your description")
            return render(request, "expenses/add_expenses.html", context)
        if not date:
            messages.error(request, "Please select a date")
            return render(request, "expenses/add_expenses.html", context)
        if not category:
            messages.error(request, "Please select a category")
            return render(request, "expenses/add_expenses.html", context)
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date,
        )
        messages.success(request, "Expense Added")
        return redirect("expenses")


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    catgories = ExpenseCategory.objects.all()
    values = {
        "amount": expense.amount,
        "description": expense.description,
        "expense_date": expense.date.strftime("%Y-%m-%d") if expense.date else "",
        "category": expense.category
    }
    context = {"expense": expense,
               "values": values,
               "categories": catgories,
               }

    if request.method == "GET":
        return render(request, "expenses/expense_edit.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
    if not amount:
        messages.error(request, "Please enter your amount")
        return render(request, "expenses/expense_edit.html", context)
    description = request.POST.get("description")
    date = request.POST.get("expense_date")
    category = request.POST.get("category")
    if not description:
        messages.error(request, "Please enter your description")
        return render(request, "expenses/expense_edit.html", context)
    if not date:
        messages.error(request, "Please select a date")
        return render(request, "expenses/expense_edit.html", context)

    expense.owner = request.user
    expense.amount = amount
    expense.description = description
    expense.category = category
    expense.date = date
    expense.save()
    messages.success(request, "Expense updated successfully")
    return redirect("expenses")


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("expenses")


def expense_category_summary(request):
    todays_date= datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses=Expense.objects.filter(owner =request.user, date__gte=six_months_ago,date__lte=todays_date)
    finalrep = {}
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount
    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)

    return JsonResponse({"expense_category_date":finalrep},safe=False)

def statsView(request):
    return render(request, "expenses/stats.html")

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = f'attachment; filename=Expenses_{current_time}.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses = Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date.strftime("%Y-%m-%d")])
    return response
def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = f'attachment; filename=Expenses_{current_time}.xlsx'

    workbook = xlsxwriter.Workbook(response,{'in_memory': True})
    worksheet = workbook.add_worksheet()
    headers=['Amount','Description','Category','Date']
    for col,header in enumerate(headers):
        worksheet.write(0,col,header)
    expenses = Expense.objects.filter(owner=request.user)
    row=1
    for expense in expenses:
        worksheet.write(row,0,expense.amount)
        worksheet.write(row,1,expense.description)
        worksheet.write(row,2,expense.category)
        worksheet.write(row,3,expense.date.strftime("%Y-%m-%d"))
        row+=1
    workbook.close()

    return response
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = f'inline; attachment; filename=Expenses_{current_time}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))['amount__sum']

    html_string = render_to_string('expenses/pdf-output.html',{'expenses':expenses,'total_expenses':sum})
    html = HTML(string=html_string)
    result=html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.seek(0)
        response.write(output.read())
    return response