from django.contrib import admin
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.models import Group
from .models import Income_model, Expenses_model, End_of_month_model, Sip_platform_model, Sip_product_model, Sip_model

admin.site.unregister(Group)
admin.site.site_header="Budget"

admin.site.register(Income_model)
admin.site.register(Expenses_model)
admin.site.register(End_of_month_model)
admin.site.register(Sip_platform_model)
admin.site.register(Sip_product_model)
admin.site.register(Sip_model)