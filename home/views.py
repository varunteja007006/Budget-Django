from smtplib import quotedata
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from numpy.lib.function_base import append; plt.rcdefaults()
import csv
from io import StringIO
import numpy as np

from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from .forms import end_of_month_form, income, expenses, sip_form, sip_product_form, sip_platform_form
from . import models
from datetime import date, time
from django.core.paginator import Paginator

today = date.today()
month = today.strftime("%m")  

def dashboard(request): 
    form_income = income()
    form_expenses = expenses()

    obj_income = models.income.objects.all().filter(date__month=month).order_by('-date')
    obj_expenses =  models.expenses.objects.all().filter(date__month=month).order_by('-time')
    
    paginator = Paginator(obj_expenses,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'form_income': form_income, 'form_expenses': form_expenses,
                 'obj_income':obj_income, 'page_obj': page_obj}

    if request.method == "POST":
        form_income = income(request.POST)
        form_expenses = expenses(request.POST)
        if form_income.is_valid():
            form_income.save()
            form_income = income()            
            context={'form_income': form_income, 'form_expenses': form_expenses, 
                        'success_income':"successfully added income",  
                        'obj_income':obj_income, 'page_obj': page_obj}
            return redirect(reverse('home:dashboard'))

        elif form_expenses.is_valid():
            form_expenses.save()
            form_expenses = expenses()
            context={'form_income': form_income, 'form_expenses': form_expenses, 
                        'success_expenses':"successfully added expenses",  
                        'obj_income':obj_income, 'page_obj': page_obj}
            return redirect(reverse('home:dashboard'))
    return render(request, 'dashboard.html',context)

def all_transactions(request):
    obj_income = models.income.objects.all().filter(date__month=month).order_by('-date') #income 
    obj_expenses =  models.expenses.objects.all().filter(date__month=month).order_by('-time') #expenses
    obj_overall_expenses =  models.expenses.objects.all().order_by('-time')
    obj_eom = models.end_of_month_model.objects.all()  #End of month
    
    #NEED to use caching 

    #Pagination
    paginator = Paginator(obj_expenses,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    

    paginator = Paginator(obj_overall_expenses,10)
    page_number = request.GET.get('page')
    page_obj_1 = paginator.get_page(page_number) 

    #salary , total expenses, end of month
    salary = 0
    for obj in obj_income:
        salary = obj.amount

    total_debit, end_of_month = 0, 0
    for obj in obj_expenses:
        debit = obj.cost
        total_debit = total_debit + debit
    end_of_month = salary-total_debit

    
    end_of_month_now=0
    for obj in obj_eom.filter(date__month=month):
        end_of_month_now = obj.end_of_month

    if obj_eom.filter(date__month=month).count() == 0:
        updated = 'False'
    elif obj_eom.filter(date__month=month).count() > 0 and end_of_month_now!=end_of_month:
        updated = 'update'
    else:
        updated = 'True'

    form_eom_now = end_of_month_form(request.POST or None,instance=obj_eom.filter(date__month=month).first())

    if 'submit' in request.POST:
        
        if 'update' == request.POST.get('submit'):
            if form_eom_now.is_valid():
                form_eom_now.save()
                return redirect(reverse('home:all-transactions'))
        
        elif 'add' == request.POST.get('submit'):
            eom_form_obj = models.end_of_month_model(end_of_month=end_of_month)
            eom_form_obj.save()
            return redirect(reverse('home:all-transactions'))

    total_eom = 0
    for obj in obj_eom:
        total_eom = total_eom + obj.end_of_month 
    

    #category wise monthly data
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
    tot_monthly_exp = [1,1,1,1,1,1,1,1]
    
    

    #overall expenses catergory wise
    overall_exp = []
    tot = 0
    for obj in obj_overall_expenses.filter(type='Dues'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0
    for obj in obj_overall_expenses.filter(type='Loan'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0
    for obj in obj_overall_expenses.filter(type='Food'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0    
    for obj in obj_overall_expenses.filter(type='Electronics'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0    
    for obj in obj_overall_expenses.filter(type='Subscriptions'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0    
    for obj in obj_overall_expenses.filter(type='Entertainment'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0        
    for obj in obj_overall_expenses.filter(type='Rent'):
        tot = tot + obj.cost
    overall_exp.append(tot)
    tot=0    
    for obj in obj_overall_expenses.filter(type='Transportation'):
        tot = tot + obj.cost
    overall_exp.append(tot)     
    if overall_exp.count(0) == 8:
        overall_exp.clear()
        overall_exp = [1,1,1,1,1,1,1,1]

    #graphs
    #category wise for this month
    types=['Dues', 'Loan', 'Food', 'Electronics', 'Subscriptions', 'Entertainment', 'Rent', 'Transportation']
    y_pos = np.arange(len(types))
    exp=[total_dues, total_loans, total_food, total_electronics, total_subscriptions, total_entertainment, total_rent, total_transportation]
    graph_category_wise_this_month = get_graph_barh(y_pos, exp,types,'Expenses','Category wise - This month','')
 

    #category wise piechart
    types=['Dues', 'Loan', 'Food', 'Electronics', 'Subscriptions', 'Entertainment', 'Rent', 'Transportation']
    graph_category_wise_overall_pie = get_graph_pie(overall_exp, types, 'Category wise - Overall')    

    #info beside the pie chart
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
    #this month expenses
    #x=[]
    #y=[]
    #for obj in obj_expenses.order_by('-date').reverse():
    #    datedb = obj.date
    #    x.append(datedb.strftime("%d"))
    #    y.append(obj.cost)
    #graph_total_expenditure = get_graph_plot(x,y,'Date','Cost','Expenditure graph - This month','red')
    #x.clear()
    #y.clear()

    #End of month graph
    x=[]
    y=[]
    for obj in obj_eom:
        datedb = obj.date
        x.append(datedb.strftime("%m"))
        y.append(obj.end_of_month)
    graph_total_eom = get_graph_plot(x,y,'Month','Amount','End of Months graph','green')

    obj_eom_rev = obj_eom.order_by('-date')              
    #contexts      
    context = {
        'obj_income': obj_income,
        'obj_eom_rev': obj_eom_rev, 
        'page_obj': page_obj, 
        'page_obj_1': page_obj_1,
        'end_of_month': end_of_month,
        'total_debit': total_debit,
        'total_eom': total_eom,
        'updated': updated,  
        'form_eom_now':form_eom_now,
        'graph_total_eom': graph_total_eom,  
        'end_of_month_now': end_of_month_now,
        'graph_category_wise_this_month': graph_category_wise_this_month, 
        'graph_category_wise_overall_pie': graph_category_wise_overall_pie,
        'types': types, 
        'overall_exp': overall_exp, 
        'category_wise_overall': category_wise_overall, 
        'category_wise_monthly_exp': category_wise_monthly_exp,
        }

    return render(request, 'all_transactions.html', context)

def sip(request):
    form_sip = sip_form(request.POST)
    form_sip_platform = sip_platform_form(request.POST)
    form_sip_product = sip_product_form(request.POST)

    obj_sip         = models.sip.objects.all().order_by('-sip_date')
    obj_product     = models.sip_product_model.objects.all()
    obj_platform    = models.sip_platform_model.objects.all()

    context = {'form_sip':form_sip, 'form_sip_platform': form_sip_platform, 'form_sip_product': form_sip_product,
                'obj_sip': obj_sip, 'obj_product': obj_product, 'obj_platform': obj_platform}

    if 'save_platform' in request.POST:
        if form_sip_platform.is_valid():
            form_sip_platform.save()
            form_sip_platform = sip_platform_form(request.POST)
        context['msg'] = "successfully added platform !!"
        return render(request, 'sip.html', context )

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
    obj_expenses =  models.expenses.objects.all().filter(date__month=month).order_by('-time')
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
    obj_expenses =  models.expenses.objects.all().order_by('-time')
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

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

def get_graph_bar(x, y, xlabel, ylabel, graph_title, colour):
    #plt.xkcd()
    fig = plt.figure()
    #colours = []
    plt.bar(x, y)
    addlabels(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(graph_title)
    plt.tight_layout()

    #plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    #plt.style.use('fivethirtyeight')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data

def get_graph_barh(y_pos, exp, types, xlabel, graph_title, colour):
    #plt.xkcd()
    fig = plt.figure()
    colours = ['#0d6efd','#6610f2','#0dcaf0','#d63384','#dc3545','#fd7e14','#ffc107','#198754']
    plt.barh(y_pos, exp, align='center', alpha=0.8, color=colours)
    plt.yticks(y_pos, types)
    plt.xlabel(xlabel)
    plt.title(graph_title)
    plt.tight_layout()

    #plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    #plt.style.use('fivethirtyeight')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data

def get_graph_plot(x, y, xlabel, ylabel, graph_title, colour):
    #plt.xkcd()
    fig = plt.figure()

    plt.plot(x, y, color=colour, label = graph_title, marker='o',linestyle='--',linewidth=0.7)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(graph_title)
    #plt.style.use('fivethirtyeight')
    plt.tight_layout()

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()

    return data   

def get_graph_pie(overall_exp, types, graph_title):
    fig = plt.figure()
    colours = ['#0d6efd','#6610f2','#0dcaf0','#d63384','#dc3545','#fd7e14','#ffc107','#33ff66']
    explode=[0, 0.2, 0.1, 0.2, 0.2, 0.2, 0, 0.1] 
    plt.pie(overall_exp, labels=types, explode=explode, colors=colours, wedgeprops={'edgecolor':'black',}, shadow= True, autopct="%1.1f%%", rotatelabels=True)
    plt.title(graph_title)
    plt.tight_layout()

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()

    return data

def calc(request):
    return render(request, 'calc.html')
