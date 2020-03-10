from django.db import models
from authentication.models import User, BaseModel
from address.models import ShippingAddress
from cart.models import ShoppingCart
from products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(User, related_name='user_order',
                             on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,
                                         related_name='user_shipping_address',
                                         null=True, blank=True)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.SET_NULL,
                             related_name='cart_order', null=True, blank=True)
    item = models.ManyToManyField(Product, through='OrderLine', related_name='ordered_items')
    total_price = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    total_items = models.PositiveIntegerField(default=0)


class OrderLine(BaseModel):
    order = models.ForeignKey(Order, related_name='order_lines',
                              on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Product, related_name='order_items',
                             on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
