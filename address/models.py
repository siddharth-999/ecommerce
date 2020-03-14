from django.db import models
from authentication.models import User, BaseModel


class ShippingAddress(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.SET_NULL,
                             related_name='user_address')
    street = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.street, self.city,
                                    self.state, self.zipcode)
