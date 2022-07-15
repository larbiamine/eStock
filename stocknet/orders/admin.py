from django.contrib import admin
from .models import ClientOrder
from .models import SupplierOrder


admin.site.register(ClientOrder)
admin.site.register(SupplierOrder)
