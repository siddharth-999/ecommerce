from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

from .models import Product, ProductImage
from .serializers import ProductCreateSerializers, ProductListSerializers, \
    ProductDetailSerializers, ProductImageSerializers
from .permissions import ProductPermission, ProductImagePermission


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, ProductPermission)
    model = Product

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializers
        elif self.action == "retrieve":
            return ProductDetailSerializers
        elif self.action == "list":
            return ProductListSerializers
        else:
            return ProductListSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ProductImagePermission,)
    model = ProductImage
    serializer_class = ProductImageSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        user = self.request.user
        return ProductImage.objects.filter(uploaded_by=user)

    def create(self, request, *args, **kwargs):
        file_list = request.FILES.getlist('images', [])
        if not file_list:
            return Response({'detail': 'Files are missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data={'image_ids': [str(i.id) for i in instance]},
                        status=status.HTTP_201_CREATED)
