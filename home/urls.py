from django.urls import path,include
from . import views

app_name='home'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('all_transactions', views.all_transactions, name='all-transactions'),
    path('sip', views.sip, name='sip-page'),
    path('calc', views.calc, name='calc-page'),
    path('download_csv', views.download_csv, name='download-csv'),
    path('download_csv_all', views.download_csv_all, name='download-csv-all'),
]