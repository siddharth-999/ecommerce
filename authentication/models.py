import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .helpers import UserManager


class Token(models.Model):
    key = models.CharField(_("Key"), max_length=200, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User Token")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(100)).decode()

    def __str__(self):
        return self.key


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name=_('Created At'))
    modified_at = models.DateTimeField(auto_now=True, db_index=True,
                                       verbose_name=_('Modified At'))

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=254, verbose_name=_('First Name'),
                                  null=True, blank=True)
    last_name = models.CharField(max_length=254, verbose_name=_('Last Name'),
                                 null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_delete = models.BooleanField(verbose_name=_('Is Delete'), default=False)
    USERNAME_FIELD = settings.AUTH_USERNAME_FIELD
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
