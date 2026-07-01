from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile,Message

def createprofile(sender,instance,created,**kwargs):

    if created:
        user = instance
        profile = Profile.objects.create(
           user = user,
           username = user.username ,
           email = user.email,
           name= user.first_name
        )
        subject = 'Welcome to my website DevSearch'
        message = f'We are glad to have {user.first_name} with us.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
        # Send internal welcome message
        try:
            system_sender = Profile.objects.get(user__username='admin')  # Change 'admin' to your actual admin username
        except Profile.DoesNotExist:
            system_sender = None  # You can also skip sending if no admin

        if system_sender:
            Message.objects.create(
                sender=system_sender,
                receiver=profile,
                subject="Welcome to DevSearch!",
                body="Hi there! 👋\n\nWelcome to DevSearch. We're glad to have you on board.\n\nFeel free to explore, build your profile, and connect with others.\n\nCheers,\nThe DevSearch Team"
            )

def updateprofile(sender,instance,created,**kwargs):
    profile = instance
    user  = profile.user
    if created==False:
        user.username = profile.username  
        user.email = profile.email
        user.first_name = profile.name
        user.save()
        




    

post_save.connect(createprofile, sender=User)
post_save.connect(updateprofile, sender=Profile)


