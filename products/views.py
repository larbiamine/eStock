from django.shortcuts import render
from .models import Product
from .forms import ProductForm,RawProductForm
# Create your views here.


def productCreateView(request):
    form= RawProductForm()
    if request.method == "POST":
        form= RawProductForm(request.POST )
    context= {
        "form": form
    }
    return render(request, "product/product_create.html", context)    



# def productCreateView(request):
#     form = ProductForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = ProductForm()
#     context= {
#         'form': form 
#     }
#     return render(request, "product/product_create.html", context)    




def productView(request):
    obj = Product.objects.get(id=2)
    context= {
        'object': obj 
    }
    return render(request, "product/product_detail.html", context)
# OR
    # context ={
    #     'Title'         : obj.Title,
    #     'Description'   : obj.Description,
    #     'PurchasePrice' : obj.PurchasePrice,
    #     'SalesPrice'    : obj.SalesPrice,
    #     'Reference'     : obj.Reference,
    #     'Manufacturer'  : obj.Manufacturer,
    #     #'Suppliers'     : obj.Suppliers,
    #     'Category'      : obj.Category,
    #     'Quantity'      : obj.Quantity
    # }

    