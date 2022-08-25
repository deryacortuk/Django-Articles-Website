from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import DailyModel

@receiver(post_save, sender=DailyModel)
def news_save_handler(sender, **kwargs):
     if settings.DEBUG:
         print(f"{kwargs['instance']} saved.")
         
@receiver(post_delete, sender=DailyModel)
def news_delete_handler(sender, **kwargs):
     if settings.DEBUG:
         print(f"{kwargs['instance']} deleted.")