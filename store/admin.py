# from django.contrib import admin
# from .models import *
# # Register your models here.


# admin.site.register(Product)
# admin.site.register(Category)
# # admin.site.register(ProductAttribute)
# # admin.site.register(ProductReview)
from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    search_fields = ['name']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'value', 'extra_price']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant', 'stock_quantity']
    search_fields = ['product__name']

@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product']
    search_fields = ['product']

# @admin.register(ProductReview)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['user', 'product', 'rating', 'created_at']
#     search_fields = ['product__name', 'user__username']
