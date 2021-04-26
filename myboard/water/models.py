from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.PositiveIntegerField(default=0)
    today = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    
@receiver(post_save, sender = User)
def rating_post_save(sender, instance, created, **kwargs ):
    if created:
        Profile.objects.cteate(user = instance)