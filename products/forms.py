from django import forms
from .models import Product
from suppliers.models import Supplier
from multiselectfield import MultiSelectField

S_CHOICES=()
for s in Supplier.objects.all():
    S_CHOICES =  ((s.Name,s.Name),) + S_CHOICES 

class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = [
            'Title',
            'Description',
            'PurchasePrice',
            'SalesPrice',
            'Reference',
            'Manufacturer',
            'Suppliers',
            'Category',
            'Quantity'

        ]

    
class RawProductForm(forms.Form):
    Title = forms.CharField()
    Description = forms.CharField(required=False, widget = forms.Textarea)
    PurchasePrice = forms.DecimalField()
    Title         = forms.CharField()
    Description   = forms.CharField( required=False, widget = forms.Textarea)
    PurchasePrice = forms.DecimalField()
    SalesPrice    = forms.DecimalField()
    Reference     = forms.CharField()
    Manufacturer  = forms.CharField()
    Suppliers     = MultiSelectField(choices=S_CHOICES)
    Category      = forms.CharField()
    Quantity      = forms.DecimalField()

    
