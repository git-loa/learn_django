from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    #Call back function 
    #sender: The model that sends the signal
    #instance: The instance of the model that triggered the signal
    #created: boolean
    #print(f'Profile instance {instance} Saved!')
    
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            username = user.username 
        )
@receiver(post_save, sender=Profile)    
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created==False:
        user.email = profile.email
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.save()
    
@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()