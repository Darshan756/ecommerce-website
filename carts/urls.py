from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add/<int:product_id>/',views.add_cart,name='add_cart'),
    path('delete/<int:cart_item_id>/',views.decrease_cart_item,name='delete_cart'),
    path('remove/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),

]
