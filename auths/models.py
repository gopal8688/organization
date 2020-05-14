# Django libraries.
from django.db import models
from django_mysql.models import EnumField
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.conf.urls.static import static


# Project libraries
from .managers import CustomUserManager

# Create your models here.
class Customer(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Prefer not say')
    ]

    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    sex = models.CharField(max_length=2, choices=SEX_CHOICE)
    password = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    pfp = models.ImageField()
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    date_joined = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    brand_name = models.CharField(max_length=150)
    brand_url = models.URLField()
    brand_logo = models.ImageField(upload_to='brand_logo/')
    org_name = models.CharField(max_length=150)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(default=None, blank=True, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'customers'

class Property(models.Model):

    pid = models.CharField(max_length=16, unique=True)
    uuid = models.CharField(max_length=150, unique=True)
    pname = models.CharField(max_length=16)
    track = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    properties = models.ManyToManyField(
        Customer,
        through='CPRelationship'
    )

    class Meta:
        db_table = 'property'

class WebPlatform(models.Model):
    domain = models.CharField(max_length=200)
    verify_code = models.CharField(max_length=50)
    verified = models.BooleanField(default=True) 
    
    properties = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    class Meta:
        db_table = 'web_platform'

class CPRelationship(models.Model):
    ROLE_CHOICE = [
        ('S', 'Owner'),
        ('A', 'Admin'),
        ('O', 'Operator'),
        ('R', 'Restricted'),
    ]

    cust = models.ForeignKey(Customer, on_delete=models.CASCADE)
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICE)

    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cprelationship'

class PropertyTokens(models.Model):
    pid = models.CharField(max_length=16)
    psecret = models.CharField(max_length=150)
    generated_by = models.IntegerField() # will have customer's id.
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    
    class Meta:
        db_table = 'property_tokens'

class DoNotTrackIP(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200)
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'do_not_track_ip'

class DoNotTrackEmail(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    email = models.CharField(max_length=150)
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'do_not_track_email'

class CustomizeAlerts(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    risk_threshold = models.CharField(max_length=150)
    app_uid = models.CharField(max_length=150)
    app_type = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customize_alerts'

class Webhooks(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.CharField(max_length=150)
    options = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'webhooks'

