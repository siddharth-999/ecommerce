from django.db import models
from authentication.models import User, BaseModel


class Product(BaseModel):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='product_added_by')
    available_stock = models.IntegerField(default=0, null=True, blank=True)
    product_price = models.DecimalField(max_digits=200, decimal_places=2, default=0)


class ProductImage(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='product_image')
    image = models.ImageField(null=True, blank=True, upload_to='products')
    uploaded_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='product_image_uploaded_by')
