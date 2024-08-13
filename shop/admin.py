from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, PromoCode, GroupDiscount

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PromoCode)
admin.site.register(GroupDiscount)
