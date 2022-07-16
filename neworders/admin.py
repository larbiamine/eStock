from django.contrib import admin
from .models import nClientOrder
from .models import nSupplierOrder
from .models import nOrderC,nOrderS


admin.site.register(nClientOrder)
admin.site.register(nSupplierOrder)
admin.site.register(nOrderS)
admin.site.register(nOrderC)
