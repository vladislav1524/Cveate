from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.account.utils import send_email_confirmation
from allauth.account.adapter import get_adapter


@receiver(user_signed_up)
def user_signed_up_from_email_confirmation(request, user, **kwargs):
    if user.email: 
        send_email_confirmation(request, user)
