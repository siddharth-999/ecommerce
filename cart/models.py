from django.db import models
from authentication.models import User, BaseModel
from products.models import Product


class ShoppingCart(BaseModel):
    user = models.OneToOneField(User, related_name='user_cart',
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    item = models.ManyToManyField(Product, through='Cart', related_name='cart_items')
    total_price = models.DecimalField(max_digits=200, decimal_places=2, default=0)

    def __str__(self):
        return str('{}'.format(self.user))


class Cart(BaseModel):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.SET_NULL,
                             related_name='user_cart', null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL,
                             related_name='cart_item', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.item)
