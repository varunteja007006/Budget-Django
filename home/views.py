from datetime import date

from .graphFunctions import GraphFunctions
from .models import Income_model, Expenses_model, Sip_model, Sip_platform_model, Sip_product_model, End_of_month_model
from .forms import End_of_month_form, Income_form, Expenses_form, Sip_form, Sip_product_form, Sip_platform_form, Sip_form

from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse

import numpy as np
from io import StringIO
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from collections import defaultdict

plt.rcdefaults()
today = date.today()
month = today.strftime("%m")
gf = GraphFunctions()

def dashboard(request):
    form_income = Income_form()
    form_expenses = Expenses_form()
    #get income only first 3 records for the current month and sorted by time
    obj_income = Income_model.objects.all().filter(
        date__month=month).order_by('-time')[:3]
    #get expenses records for the month
    obj_expenses = Expenses_model.objects.all().filter(
        date__month=month).order_by('-time')[:8]
    # paginator for the expenses
    paginator = Paginator(obj_expenses, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'form_income': form_income, 'form_expenses': form_expenses,
               'obj_income': obj_income, 'page_obj': page_obj, 'title': 'Dashboard'}

    if request.method == "POST":
        form_income = Income_form(request.POST)
        form_expenses = Expenses_form(request.POST)
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
    obj_income = Income_model.objects.all().filter(
        date__month=month).order_by('-time')  
    
    # get expenses filtered by current month and sorted by time
    obj_overall_expenses = Expenses_model.objects.all().order_by('-time') 

    # get expenses filtered by current month and sorted by time
    obj_expenses = obj_overall_expenses.filter(
        date__month=month)
    
    # get all EOM(End Of Month) records
    obj_eom = End_of_month_model.objects.all() 

    # All the End of Month records - Latest to Oldest
    obj_eom_rev = obj_eom.order_by('-date')

    # Pagination for the current month expenses
    paginator = Paginator(obj_expenses, 10)
    page_number = request.GET.get('page')
    expenses_page_obj = paginator.get_page(page_number)

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
    form_eom_now = End_of_month_form(
        request.POST or None, instance=obj_eom.filter(date__month=month).first())

    if 'submit' in request.POST:

        if 'update' == request.POST.get('submit'):
            if form_eom_now.is_valid():
                form_eom_now.save()
                return redirect(reverse('home:all-transactions'))

        elif 'add' == request.POST.get('submit'):
            eom_form_obj = End_of_month_model(end_of_month=end_of_month)
            eom_form_obj.save()
            return redirect(reverse('home:all-transactions'))
    
    expenses_type_list = ['Dues', 'Loan', 'Food', 'Electronics', 'Subscriptions', 'Entertainment', 'Rent', 'Transportation']
    
    #Get expenses categorised by type
    monthly_expenses_by_type = dict.fromkeys(expenses_type_list, 0)
    for item in expenses_type_list:
        for obj in obj_expenses.filter(type=item):
            monthly_expenses_by_type[item] += obj.cost
    
    #Get overall expenses categorised by type
    overall_expenses_by_type = dict.fromkeys(expenses_type_list, 0)
    for item in expenses_type_list:
        for obj in obj_overall_expenses.filter(type=item):
            overall_expenses_by_type[item] += obj.cost

    # graphs
    # category wise for this month
    y_pos = np.arange(len(expenses_type_list))
    graph_category_wise_this_month = gf.get_graph_barh(
        y_pos, list(monthly_expenses_by_type.values()), expenses_type_list, 'Expenses', 'Category wise - This month')

    # Overall expense piechart
        #remove the '0' valued keys in overall_expenses_by_type dictionary & save it to filtered_overall_expenses_by_type dictionary.
    filtered_overall_expenses_by_type = {}
    for key, value in overall_expenses_by_type.items():
        if value!=0:
            filtered_overall_expenses_by_type[key] = value
    
    # Overall expense piechart
    graph_pie_overall_expenses_by_type = gf.get_graph_pie(
        list(filtered_overall_expenses_by_type.values()), list(filtered_overall_expenses_by_type.keys()), '')

    #Month End Savings graph plot
    x = []
    y = []
    for obj in obj_eom:
        x.append(obj.date.strftime("%b-%Y"))
        y.append(obj.end_of_month)
    graph_total_eom = gf.get_graph_plot(
        x, y, '', 'Amount saved', 'Savings graph', 'green')
    
    # contexts
    context = {
        'obj_income': obj_income,
        'obj_eom_rev': obj_eom_rev,
        'expenses_page_obj': expenses_page_obj,
        'salary': salary, # Present month salary.
        'total_expenses': total_expenses, #expense for the present month.
        'end_of_month': end_of_month, # End of month for the present month calculated from the difference of salary and total expenses.
        'end_of_month_noted': end_of_month_noted, #End of month of the latest record stored in DB.
        'total_eom': total_eom, # overall End of month calculated by adding all the End of month records in DB.
        'need_to_update': need_to_update, # Update flag when end_of_month does not match end_of_month_noted.
        'form_eom_now': form_eom_now,
        #data for the tables
        'overall_expenses_by_type_data': overall_expenses_by_type.items(),
        'monthly_expenses_by_type_data': monthly_expenses_by_type.items(),
        #graphs
        'graph_total_eom': graph_total_eom,
        'graph_category_wise_this_month': graph_category_wise_this_month,
        'graph_pie_overall_expenses_by_type': graph_pie_overall_expenses_by_type,
    }

    return render(request, 'all_transactions.html', context)

def sip(request):
    form_sip = Sip_form(request.POST)
    form_sip_platform = Sip_platform_form(request.POST)
    form_sip_product = Sip_product_form(request.POST)

    obj_sip = Sip_model.objects.all().order_by('-sip_date')
    obj_product = Sip_product_model.objects.all()
    obj_platform = Sip_platform_model.objects.all()

    context = {'form_sip': form_sip, 'form_sip_platform': form_sip_platform, 'form_sip_product': form_sip_product,
               'obj_sip': obj_sip, 'obj_product': obj_product, 'obj_platform': obj_platform}

    if 'save_platform' in request.POST:
        if form_sip_platform.is_valid():
            form_sip_platform = Sip_platform_form(request.POST)
            form_sip_platform.save()
        context['msg'] = "successfully added platform !!"
        return render(request, 'sip.html', context)

    elif 'save_product' in request.POST:
        if form_sip_product.is_valid():
            form_sip_product = Sip_product_form(request.POST)
            form_sip_product.save()
        context['msg'] = "successfully added product !!"
        return render(request, 'sip.html', context)

    elif 'save_sip' in request.POST:
        if form_sip.is_valid():
            form_sip = Sip_form(request.POST)
            form_sip.save()
        context['msg'] = "successfully added SIP !!"
        return render(request, 'sip.html', context)

    return render(request, 'sip.html', context)

def download_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="budget.csv"'},
    )
    obj_expenses = Expenses_model.objects.all().filter(
        date__month=month).order_by('-time')
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

def download_csv_all(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="all_budget.csv"'},
    )
    obj_expenses = Expenses_model.objects.all().order_by('-time')
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
