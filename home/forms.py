from typing import Type
from django.db.models import fields
from django import forms
from django.forms import ModelForm, widgets

from django.forms.models import ModelChoiceField
from .models import Income_model, Expenses_model, End_of_month_model, Sip_platform_model, Sip_product_model, Sip_model

class Income_form(ModelForm):
    class Meta:
        model = Income_model
        fields = ['name','amount','comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control',})
        self.fields['comment'].widget.attrs.update({'rows': 2})
        self.fields['amount'].widget.attrs.update({'class': 'form-control',})
        self.fields['name'].widget.attrs.update({'class': 'form-control',})

class Expenses_form(ModelForm):
    class Meta:
        model = Expenses_model
        fields = ['name','type','necessity','cost','comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control',})
        self.fields['comment'].widget.attrs.update({'rows': 2})
        self.fields['cost'].widget.attrs.update({'class': 'form-control',})
        self.fields['name'].widget.attrs.update({'class': 'form-control',})
        self.fields['type'].widget.attrs.update({'class': 'form-select',})
        self.fields['necessity'].widget.attrs.update({'class': 'form-select',})

class End_of_month_form(ModelForm):
    class Meta:
        model = End_of_month_model
        fields = ['end_of_month']

class Sip_platform_form(ModelForm):
    class Meta:
        model = Sip_platform_model
        fields = ['sip_platformname']

class Sip_product_form(ModelForm):
    class Meta:
        model = Sip_product_model
        fields = ['sip_productname']

class DateInput(forms.DateInput):
    input_type = 'date'
    
class Sip_form(ModelForm):
    class Meta:
        model = Sip_model
        fields = ['sip_platform_name', 'sip_product_name', 'amount', 'sip_date', 'comment']
        widgets = {'sip_date': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sip_platform_name'].widget.attrs.update({'class': 'form-select',})
        self.fields['sip_product_name'].widget.attrs.update({'class': 'form-select',})
        self.fields['sip_date'].widget.attrs.update({'class': 'form-control',})
