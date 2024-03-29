
"""stocknet URL Configuration
cycle
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from django.urls import path,include
from products.views import productView,productCreateView
urlpatterns = i18n_patterns(
    path('rosetta/', include('rosetta.urls')),
    path('',include('appp.urls')), # home contact about learnmore and services pages all in there
    path('',include('neworders.urls')), # home contact about learnmore and services pages all in there
    path('admin/', admin.site.urls),
      # NEW
    path('accounts/',include('accounts.urls')),# login register (contact related) pages 
    path('product/',productView),
    path('createproduct/',productCreateView),
    path('bootstrap/',TemplateView.as_view(template_name='bootstrap/example.html'))
    
)
