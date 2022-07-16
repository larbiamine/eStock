from django.shortcuts import render
from .forms import nOrderCForm
from .models import nOrderS,nOrderC,nSupplierOrder,nClientOrder
from django.http import JsonResponse
from django.template.loader import render_to_string

def nOrderC_list(request):
    nOrderCs = nOrderC.objects.all()
    return render(request, 'dashboard/order/Nordercreate.html', {'nOrderCs': nOrderCs})
