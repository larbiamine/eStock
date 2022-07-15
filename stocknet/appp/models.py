from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=100,default='TITLE')
    desc = models.TextField(default='DESC')
    ico = models.ImageField(upload_to='pics',default='NULL')
