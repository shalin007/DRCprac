
""" EmailPhoneUser models."""
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    """ Custom Manager for EmailPhoneUser.
    For Examples check Django code:
    https://github.com/django/django/blob/master/django/contrib/auth/models.py
    """
  

    def _create_user(self, email_or_phone, password,is_staff,is_superuser, **extra_fields):
        
        """ Create CustomUser with the given email or phone and password.
        :param str email_or_phone: user email or phone
        :param str password: user password
   
        :return settings.AUTH_USER_MODEL user: user
        :raise ValueError: email or phone is not set
        :raise NumberParseException: phone does not have correct format
        """
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)
            username, email, phone = (email_or_phone, email_or_phone, "")
        else:
            username, email, phone = (email_or_phone, "", email_or_phone)

      
        user = self.model(
            username=username,
            email=email,
            phone=phone,
            **extra_fields
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password,False,False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password,True,True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """ Abstract User with the same behaviour as Django's default User."""

    username = models.CharField(_('email or phone'), max_length=255, unique=True,)
    email = models.EmailField(_('email'), max_length=254, blank=True)
    sec_email = models.EmailField(_('secondary email'), max_length=254, blank=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True)
    location = models.CharField(_('phone'), max_length=255, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
