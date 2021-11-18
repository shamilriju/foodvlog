from django.db import models
from shamart.models import *
from django.contrib.auth.models import User
# Create your models here.
class cartlist(models.Model):
    cart_id=models.CharField(max_length=100,unique=True)

    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class items(models.Model):
    prod=models.ForeignKey(products,on_delete=models.CASCADE)
    cart=models.ForeignKey(cartlist,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.prod

    def total(self):
        return self.prod.price*self.quantity
