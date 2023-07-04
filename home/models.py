from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import TimeField
from django.utils import timezone
from datetime import date

# Create your models here.
class Income_model(models.Model):
    name = models.CharField(max_length=150)
    amount = models.IntegerField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.localtime)
    comment = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Expenses_model(models.Model):
    name = models.CharField(max_length=150)
    Type_Choices = [
        ('Dues', 'Dues'),
        ('Loan', 'Loan'),
        ('Food', 'Food'),
        ('Electronics', 'Electronics'),
        ('Subscriptions', 'Subscriptions'),
        ('Entertainment', 'Entertainment'),
        ('Rent', 'Rent'),
        ('Transportation', 'Transportation')]
    type = models.CharField(max_length=50,choices=Type_Choices,default="Entertainment")
    
    Necessity_Choices = [
        ('Need', 'Need'),
        ('Want', 'Want'),
    ]
    necessity = models.CharField(max_length=50,choices=Necessity_Choices,default="Need")
    
    cost = models.IntegerField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.localtime)
    comment = models.TextField(blank=True)
   
    def __str__(self):
        return self.name

class End_of_month_model(models.Model):
    end_of_month = models.IntegerField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.localtime)

    def __str__(self):
        #End Of Month (EOM)
        return 'EOM_'+str(self.date)+'_'+str(self.time)

#Below are SIP related transactions
#Platform used to invest
class Sip_platform_model(models.Model):
    sip_platformname = models.CharField(max_length=250)

    def __str__(self):
        return self.sip_platformname

#SIP products or fund manager
class Sip_product_model(models.Model):
    sip_productname = models.CharField(max_length=250)
    
    def __str__(self):
        return self.sip_productname

#SIP Transaction model    
class Sip_model(models.Model):
    sip_platform_name = models.ForeignKey(Sip_platform_model, on_delete=models.CASCADE)
    sip_product_name = models.ForeignKey(Sip_product_model, on_delete=models.CASCADE)
    amount = models.IntegerField()
    sip_date = models.DateField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.localtime)
    comment = models.TextField(blank=True)

    def __str__(self):
        name = "SIP_"+str(self.sip_date)
        return name