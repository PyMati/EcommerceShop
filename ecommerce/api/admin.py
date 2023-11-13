from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProductCategory, Product, Address, Order, UserProfile


class CustomAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_customer", "is_seller")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Client-Seller",
            {
                "fields": ("is_customer", "is_seller"),
            },
        ),
    )


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(UserProfile, CustomAdmin)
