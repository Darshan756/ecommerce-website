from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name     = models.CharField(max_length=200,unique=True)
    slug             = models.SlugField(max_length=200,unique=True)
    description      = models.TextField(max_length=500,blank=True)
    price            = models.IntegerField()
    images           = models.ImageField(upload_to='photos/products')
    stock            = models.IntegerField()
    is_available     = models.BooleanField(default=True)
    category         = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date     = models.DateTimeField(auto_now_add=True)
    modiefied_date   = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('products_details',args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name
variation_category_choices = (
    ('color','color'),
    ('size','size')
)

class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager,self).filter(variation_categories = 'color',is_active=True)
    def  size(self):
        return super(VariationManager,self).filter(variation_categories = 'size',is_active=True)

class Variantions(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variation')
    variation_categories = models.CharField(max_length=250,choices=variation_category_choices)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    objects = VariationManager()
    class Meta:
        ordering = ['variation_categories', 'variation_value']
    def __str__(self):
        return self.variation_value
    
