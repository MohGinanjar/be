from django.db import models

# Create your models here.
from django.db import models
from app.helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (PermissionsMixin, UserManager, AbstractBaseUser)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import jwt
from datetime import datetime,  timedelta
from django.conf import settings

# test

class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin,TrackingModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified=models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this user email is verified. "
        ),
    )
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    
    
    @property
    def token(self):
        token = jwt.encode(
            {'username': self.username, 'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token
    
    


class AttedanceWorkTime(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True,)
    date = models.DateField(max_length=12,blank= True,null=True)
    time = models.TimeField(max_length=12)
    type_absen = models.CharField(max_length=10)
    desc = models.TextField()
    emp = models.ForeignKey(to=User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name
    
    
class AttedanceTimeView(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True,)
    date = models.DateField(max_length=12,blank= True,null=True)
    time_in = models.TimeField(max_length=12, blank=True, null=True)
    time_out = models.TimeField(max_length=12, blank=True, null=True)
    type_absen = models.CharField(max_length=10)
    emp = models.ForeignKey(to=User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    
class ListProject(models.Model):
    name_project = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name_project
    

class ProjectDescription(models.Model):
    emp = models.ForeignKey(to=User, on_delete=models.CASCADE)
    choice_project = models.ForeignKey(to=ListProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True,)
    date = models.DateField(max_length=12,blank= True,null=True)
    time_in = models.TimeField(max_length=12, blank=True, null=True)
    time_out = models.TimeField(max_length=12, blank=True, null=True)
    type_absen = models.CharField(max_length=10)
    lat =  models.CharField(max_length=20)
    lon =  models.CharField(max_length=20)
    detail_project = models.TextField()
    status = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.emp} {self.choice_project}'