from django.db.models.signals import post_save

from .models import User, Token


def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


post_save.connect(create_auth_token, sender=User)
