from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

@api_view(["GET"])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response({"success": True, "data": serializer.data})

@api_view(["GET"])
def search_products(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=q)
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response({"success": True, "data": serializer.data})
