from django.contrib import admin
from .models import Category

class CategoryAdimn(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')
admin.site.register(Category,CategoryAdimn)