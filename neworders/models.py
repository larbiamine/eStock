from django.db import models
from products.models import Product
from clients.models import Client
from suppliers.models import Supplier

from django.contrib.auth.models import User

Values = [
    ('en attente', 'en attente'),
    ('livré', 'livré'),
]

class nClientOrder(models.Model):
    
    Client        = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="nclientorderlist", null=True) # <--- added 
    Date          = models.DateField(null=True)
    Status        = models.CharField(max_length=20, choices=Values , blank=False, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nclientorderlist", null=True) # <--- added
    Total         = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    
  

class nSupplierOrder(models.Model):
    
    Supplier      = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="nsupplierorderlist", null=True) # <--- added 
    Date          = models.DateField( null=True)
    Status        = models.CharField(max_length=20, choices=Values, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nsupplierorderlist", null=True) # <--- added
    Total         = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)


class nOrderC(models.Model):
    nClientOrder    = models.ForeignKey(nClientOrder, on_delete=models.CASCADE, related_name="norderclist", null=True)
    Product         = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="norderclist", null=True) # <--- added
    Quantity        = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="norderclist", null=True) # <--- added
    
    def line_total(self):
        return self.Quantity * self.Product.SalesPrice


class nOrderS(models.Model):
    nSupplierOrder  = models.ForeignKey(nSupplierOrder, on_delete=models.CASCADE, related_name="norderslist", null=True)
    Product         = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="norderslist", null=True) # <--- added
    Quantity        = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="norderslist", null=True) # <--- added
    
    def line_total(self):
        return self.Quantity * self.Product.SalesPrice