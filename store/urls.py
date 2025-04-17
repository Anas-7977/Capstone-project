from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'inventory', InventoryViewSet)
# router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('products/', product_listing, name='product_listing'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('cart/', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart-page/', cart_view, name='cart-page'),

]
