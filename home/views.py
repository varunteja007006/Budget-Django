from datetime import date

from .graphFunctions import GraphFunctions
from . import models
from .forms import end_of_month_form, Income, expenses, sip_form, sip_product_form, sip_platform_form

from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse

import numpy as np
from io import StringIO
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

plt.rcdefaults()
today = date.today()
month = today.strftime("%m")
gf = GraphFunctions()

def dashboard(request):
    form_income = Income()
    form_expenses = expenses()
    #get income only first 3 records for the current month and sorted by time
    obj_income = models.Income.objects.all().filter(
        date__month=month).order_by('-time')[:3]
    #get expenses records for the month
    obj_expenses = models.expenses.objects.all().filter(
        date__month=month).order_by('-time')[:8]
    # paginator for the expenses
    paginator = Paginator(obj_expenses, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'form_income': form_income, 'form_expenses': form_expenses,
               'obj_income': obj_income, 'page_obj': page_obj, 'title': 'Dashboard'}

    if request.method == "POST":
        form_income = Income(request.POST)
        form_expenses = expenses(request.POST)
        #check for the income form
        if form_income.is_valid():
            form_income.save()
            #redirect to homepage/dashboard
            return redirect(reverse('home:dashboard'))
        #check for the expenses form
        elif form_expenses.is_valid():
            form_expenses.save()
            #redirect to homepage/dashboard
            return redirect(reverse('home:dashboard'))
    return render(request, 'dashboard.html', context)


def all_transactions(request):
    # get income filtered by current month and sorted by time
    obj_income = models.Income.objects.all().filter(
        date__month=month).order_by('-time')  
    
    # get expenses filtered by current month and sorted by time
    obj_expenses = models.expenses.objects.all().filter(
        date__month=month).order_by('-time') 
    
    # get all expenses sorted by time
    obj_overall_expenses = models.expenses.objects.all().order_by('-time')
    
    # get all EOM(End Of Month) records
    obj_eom = models.end_of_month_model.objects.all() 

    # Pagination for the current month expenses
    paginator = Paginator(obj_expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # salary , total expenses, end of month, end of month last noted, total calculated end of month value
    salary, total_expenses, end_of_month, end_of_month_noted, total_eom= 0, 0, 0, 0, 0
    
    #total salary
    for obj in obj_income:
        salary += obj.amount
    
    #total expenses
    for obj in obj_expenses:
        total_expenses += obj.cost
    
    #End Of Month after deducting total expenses from salary
    end_of_month = salary-total_expenses

    #total End Of Month
    for obj in obj_eom:
        total_eom = total_eom + obj.end_of_month

    #End Of Month from the last record in db
    end_of_month_noted = 0
    latest_obj_eom = obj_eom.filter(date__month=month).order_by('-time').first()
    if latest_obj_eom is None: 
        end_of_month_noted = 0
    else:
        end_of_month_noted = latest_obj_eom.end_of_month   

    #Checking if the End Of Month record needs to be updated or not
    # No End Of Month record    
    if obj_eom.filter(date__month=month).count() == 0:
        need_to_update = 'False'

    # End Of Month record is available but it is not updated to current End Of Month
    elif obj_eom.filter(date__month=month).count() > 0 and end_of_month_noted != end_of_month:
        need_to_update = 'update'

    #End Of Month is up to date
    else:
        need_to_update = 'True'

    #Form to update the End of Month
    form_eom_now = end_of_month_form(
        request.POST or None, instance=obj_eom.filter(date__month=month).first())

    if 'submit' in request.POST:

        if 'update' == request.POST.get('submit'):
            if form_eom_now.is_valid():
                form_eom_now.save()
                return redirect(reverse('home:all-transactions'))

        elif 'add' == request.POST.get('submit'):
            eom_form_obj = models.end_of_month_model(end_of_month=end_of_month)
            eom_form_obj.save()
            return redirect(reverse('home:all-transactions'))



    # category wise monthly data
    tot_monthly_exp = []
    total_dues = 0
    for obj in obj_expenses.filter(type='Dues'):
        total_dues = total_dues + obj.cost
    tot_monthly_exp.append(total_dues)

    total_loans = 0
    for obj in obj_expenses.filter(type='Loan'):
        total_loans = total_loans + obj.cost
    tot_monthly_exp.append(total_loans)

    total_food = 0
    for obj in obj_expenses.filter(type='Food'):
        total_food = total_food + obj.cost
    tot_monthly_exp.append(total_food)

    total_electronics = 0
    for obj in obj_expenses.filter(type='Electronics'):
        total_electronics = total_electronics + obj.cost
    tot_monthly_exp.append(total_electronics)

    total_subscriptions = 0
    for obj in obj_expenses.filter(type='Subscriptions'):
        total_subscriptions = total_subscriptions + obj.cost
    tot_monthly_exp.append(total_subscriptions)

    total_entertainment = 0
    for obj in obj_expenses.filter(type='Entertainment'):
        total_entertainment = total_entertainment + obj.cost
    tot_monthly_exp.append(total_entertainment)

    total_rent = 0
    for obj in obj_expenses.filter(type='Rent'):
        total_rent = total_rent + obj.cost
    tot_monthly_exp.append(total_rent)

    total_transportation = 0
    for obj in obj_expenses.filter(type='Transportation'):
        total_transportation = total_transportation + obj.cost
    tot_monthly_exp.append(total_transportation)

    if tot_monthly_exp.count(0) == 8:
        tot_monthly_exp.clear()
    tot_monthly_exp = [1, 1, 1, 1, 1, 1, 1, 1]

    # overall expenses catergory wise
    overall_exp = []
    tot = 0
    for obj in obj_overall_expenses.filter(type='Dues'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Loan'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Food'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Electronics'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Subscriptions'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Entertainment'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Rent'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot = 0
    for obj in obj_overall_expenses.filter(type='Transportation'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    if overall_exp.count(0) == 8:
        overall_exp.clear()
        overall_exp = [1, 1, 1, 1, 1, 1, 1, 1]

    # graphs
    # category wise for this month
    types = ['Dues', 'Loan', 'Food', 'Electronics',
             'Subscriptions', 'Entertainment', 'Rent', 'Transportation']
    y_pos = np.arange(len(types))
    exp = [total_dues, total_loans, total_food, total_electronics,
           total_subscriptions, total_entertainment, total_rent, total_transportation]
    graph_category_wise_this_month = gf.get_graph_barh(
        y_pos, exp, types, 'Expenses', 'Category wise - This month')

    # category wise piechart
    types = ['Dues', 'Loan', 'Food', 'Electronics',
             'Subscriptions', 'Entertainment', 'Rent', 'Transportation']
    graph_category_wise_overall_pie = gf.get_graph_pie(
        overall_exp, types, 'Category wise - Overall')

    # info beside the pie chart
    category_wise_overall = []
    a = []
    for i in range(len(types)):
        a.append(types[i])
        a.append(overall_exp[i])
        category_wise_overall.append(a)
        a = []

    category_wise_monthly_exp = []
    a = []
    for i in range(len(types)):
        a.append(types[i])
        a.append(tot_monthly_exp[i])
        category_wise_monthly_exp.append(a)
        a = []

    x = []
    y = []
    for obj in obj_eom:
        datedb = obj.date
        x.append(datedb.strftime("%m"))
        y.append(obj.end_of_month)
    graph_total_eom = gf.get_graph_plot(
        x, y, 'Month', 'Amount', 'End of Months graph', 'green')

    obj_eom_rev = obj_eom.order_by('-date')
    # contexts
    context = {
        'obj_income': obj_income,
        'obj_eom_rev': obj_eom_rev,
        'page_obj': page_obj,
        'salary': salary,
        'end_of_month': end_of_month,
        'total_expenses': total_expenses,
        'total_eom': total_eom,
        'need_to_update': need_to_update,
        'form_eom_now': form_eom_now,
        'end_of_month_noted': end_of_month_noted,
        'types': types,
        'overall_exp': overall_exp,
        'category_wise_overall': category_wise_overall,
        'category_wise_monthly_exp': category_wise_monthly_exp,
        'graph_total_eom': graph_total_eom,
        'graph_category_wise_this_month': graph_category_wise_this_month,
        'graph_category_wise_overall_pie': graph_category_wise_overall_pie,
    }

    return render(request, 'all_transactions.html', context)


def sip(request):
    form_sip = sip_form(request.POST)
    form_sip_platform = sip_platform_form(request.POST)
    form_sip_product = sip_product_form(request.POST)

    obj_sip = models.sip.objects.all().order_by('-sip_date')
    obj_product = models.sip_product_model.objects.all()
    obj_platform = models.sip_platform_model.objects.all()

    context = {'form_sip': form_sip, 'form_sip_platform': form_sip_platform, 'form_sip_product': form_sip_product,
               'obj_sip': obj_sip, 'obj_product': obj_product, 'obj_platform': obj_platform}

    if 'save_platform' in request.POST:
        if form_sip_platform.is_valid():
            form_sip_platform.save()
            form_sip_platform = sip_platform_form(request.POST)
        context['msg'] = "successfully added platform !!"
        return render(request, 'sip.html', context)

    elif 'save_product' in request.POST:
        if form_sip_product.is_valid():
            form_sip_product.save()
            form_sip_product = sip_product_form(request.POST)
        context['msg'] = "successfully added product !!"
        return render(request, 'sip.html', context)

    elif 'save_sip' in request.POST:
        if form_sip.is_valid():
            form_sip.save()
            form_sip = sip_form(request.POST)
        context['msg'] = "successfully added SIP !!"
        return render(request, 'sip.html', context)

    return render(request, 'sip.html', context)


def download_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="budget.csv"'},
    )
    obj_expenses = models.expenses.objects.all().filter(
        date__month=month).order_by('-time')
    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Cost', 'Date', 'Time', 'Comment'])
    for obj in obj_expenses:
        name = obj.name
        type = obj.type
        cost = obj.cost
        datedb = obj.date
        time = obj.time
        comment = obj.comment
        writer.writerow([name, type, cost, datedb, time, comment])
    return response


def download_csv_all(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="all_budget.csv"'},
    )
    obj_expenses = models.expenses.objects.all().order_by('-time')
    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Cost', 'Date', 'Time', 'Comment'])
    for obj in obj_expenses:
        name = obj.name
        expense_type = obj.type
        cost = obj.cost
        datedb = obj.date
        time = obj.time
        comment = obj.comment
        writer.writerow([name, expense_type, cost, datedb, time, comment])
    return response

def calc(request):
    return render(request, 'calc.html')
