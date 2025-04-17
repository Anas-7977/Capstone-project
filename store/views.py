from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Category, Product, ProductVariant, Inventory
from .serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer, InventorySerializer

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Product Variant ViewSet
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

# Inventory ViewSet
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

# Review ViewSet
# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

def home(request):
    featured_products = Product.objects.filter()[:6]  # Get featured products
    categories = Category.objects.all()  # Get all categories
    # promotions = Promotion.objects.all()  # Get all promotions

    context = {
        'featured_products': featured_products,
        'categories': categories,
        # 'promotions': promotions,
    }
    
    return render(request, 'home.html', context)

def product_listing(request):
    products = Product.objects.all()
    return render(request, 'plp.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.exclude(id=product_id)[:4]  # Mock logic
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })



from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q
from .documents import ProductDocument

class ProductSearchView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        category = request.GET.get("category")
        brand = request.GET.get("brand")
        sort_by = request.GET.get("sort_by", "created_at")  # or price, name
        order = request.GET.get("order", "desc")

        es_query = Q("multi_match", query=query, fields=["name", "description"]) if query else Q("match_all")

        filters = []
        if category:
            filters.append(Q("term", category=category))
        if brand:
            filters.append(Q("term", brand=brand))

        final_query = Q("bool", must=es_query, filter=filters)

        s = ProductDocument.search().query(final_query)

        # Sorting
        if sort_by:
            order_prefix = "-" if order == "desc" else ""
            s = s.sort(f"{order_prefix}{sort_by}")

        response = s.execute()

        products = [
            {
                "id": hit.meta.id,
                "name": hit.name,
                "description": hit.description,
                "price": hit.price,
                "brand": hit.brand,
                "category": hit.category,
                "sku": hit.sku,
            }
            for hit in response
        ]

        return Response(products)
    

from rest_framework import generics, permissions
from .models import Cart
from .serializers import CartSerializer

class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    

from django.shortcuts import render
from .models import Cart

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})
    
