from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.TextField(max_length=500, blank=False)
	city = models.CharField(max_length=50, blank=False)
	last_notif_check = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.username}\'s Profile'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()