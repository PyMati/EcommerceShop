from django.contrib import admin
from .models import ProductCategory, Product, Address, Order


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
