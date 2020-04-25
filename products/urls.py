from django.urls import path
from rest_framework import routers
from .views import ProductViewSet,ProductImageViewSet

app_name = 'products'

router = routers.DefaultRouter()
router.register('product', ProductViewSet, basename='product_image')
router.register('product_image', ProductImageViewSet, basename='product-image')

urlpatterns = router.urls