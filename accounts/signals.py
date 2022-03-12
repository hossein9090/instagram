from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

from .models import Account


@receiver(post_save, sender=User)
def create_authors(sender, instance, created, **kwargs):
    if created:
        try:
            Account.objects.create(user=instance)

        except:
            instance.delete()

