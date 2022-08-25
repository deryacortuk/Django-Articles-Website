from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Article

@receiver(post_save, sender=Article)
def news_save_handler(sender, **kwargs):
     if settings.DEBUG:
         print(f"{kwargs['instance']} saved.")
         
@receiver(post_delete, sender=Article)
def news_delete_handler(sender, **kwargs):
     if settings.DEBUG:
         print(f"{kwargs['instance']} deleted.")