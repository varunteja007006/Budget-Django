from django.contrib import admin
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.models import Group
from .models import income, expenses, end_of_month_model, sip_platform_model, sip_product_model, sip

admin.site.unregister(Group)
admin.site.site_header="Budget"

admin.site.register(income)
admin.site.register(expenses)
admin.site.register(end_of_month_model)
admin.site.register(sip_platform_model)
admin.site.register(sip_product_model)
admin.site.register(sip)