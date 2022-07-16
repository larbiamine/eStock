from django.db import models
from suppliers.models import Supplier
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

class Product(models.Model):
    Title         = models.CharField(max_length=100)
    Description   = models.CharField(max_length=300, null = True)
    PurchasePrice = models.DecimalField(decimal_places=2, max_digits=20,default=0)
    SalesPrice    = models.DecimalField(decimal_places=2, max_digits=20,default=0)
    Reference     = models.CharField(max_length=100)
    Manufacturer  = models.CharField(max_length=100)
    Suppliers     = models.ManyToManyField(Supplier)
    Category      = models.CharField(max_length=100)
    Quantity      = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productlist", null=True) # <--- added
    
    def __str__(self):
        return self.Title    

class StockTrack(models.Model):
    Stock         = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True) 
    In            = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True) 
    Out           = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True) 
    Date          = models.DateField( null=True)  
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stocktracklist", null=True) # <--- added
