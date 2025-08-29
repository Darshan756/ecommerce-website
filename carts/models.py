from django.db import models
from store.models import Product,Variantions
from account.models import CustomUser
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)

    date_added = models.DateField(auto_now_add=True)
   
    def __str__(self):
        return f'{self.cart_id} {self.user}'
    
class CartItem(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variantions,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product.product_name