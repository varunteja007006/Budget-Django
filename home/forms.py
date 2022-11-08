from typing import Type
from django.db.models import fields
from django import forms
from django.forms import ModelForm, widgets

from django.forms.models import ModelChoiceField
from .models import income, expenses, end_of_month_model, sip_platform_model, sip_product_model, sip

class income(ModelForm):
    class Meta:
        model = income
        fields = ['name','amount','comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control',})
        self.fields['comment'].widget.attrs.update({'rows': 2})
        self.fields['amount'].widget.attrs.update({'class': 'form-control',})
        self.fields['name'].widget.attrs.update({'class': 'form-control',})

class expenses(ModelForm):
    class Meta:
        model = expenses
        fields = ['name','type','necessity','cost','comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control',})
        self.fields['comment'].widget.attrs.update({'rows': 2})
        self.fields['cost'].widget.attrs.update({'class': 'form-control',})
        self.fields['name'].widget.attrs.update({'class': 'form-control',})
        self.fields['type'].widget.attrs.update({'class': 'form-select',})
        self.fields['necessity'].widget.attrs.update({'class': 'form-select',})

class end_of_month_form(ModelForm):
    class Meta:
        model = end_of_month_model
        fields = ['end_of_month']

class sip_platform_form(ModelForm):
    class Meta:
        model = sip_platform_model
        fields = ['sip_platformname']

class sip_product_form(ModelForm):
    class Meta:
        model = sip_product_model
        fields = ['sip_productname']

class DateInput(forms.DateInput):
    input_type = 'date'
class sip_form(ModelForm):
    class Meta:
        model = sip
        fields = ['sip_platform_name', 'sip_product_name', 'amount', 'sip_date', 'comment']
        widgets = {'sip_date': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sip_platform_name'].widget.attrs.update({'class': 'form-select',})
        self.fields['sip_product_name'].widget.attrs.update({'class': 'form-select',})
        self.fields['sip_date'].widget.attrs.update({'class': 'form-control',})
