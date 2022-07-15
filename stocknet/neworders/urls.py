from django.conf.urls import url, include
from appp.views import nClientOrder_create
from . import views
from django.urls import path
urlpatterns = [
    path('norderc_list/', views.nOrderC_list, name='nOrderC_list'),
    path('nClientOrder_create/', nClientOrder_create, name='nClientOrder_create'),

]