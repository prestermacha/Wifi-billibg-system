from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from companies.models import Company
from .manager import UserManagement
import pyotp
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone
# Create your models here.

USER_TYPE=(
    ('super_admin','Super Admin'),
    ('paltform_staff','Platform Staff'),
    ('tenant_admin','Tenant Admin'),   
    ('tenant_member','Tenant Member'),
)
phone_regex = RegexValidator(
        regex=r'^(?:\+?\d{1,3}\s?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$',
        message="Phone number must be in a valid format, e.g., +225 123-456-7890, (123) 456-7890, or 1234567890."
    )
 
class AccountUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True,verbose_name=(_('Email')))
    phone_number=models.CharField(max_length=20,validators=[phone_regex],unique=True,verbose_name=(_('Phone Number')))
    user_type=models.CharField(max_length=100,choices=USER_TYPE,verbose_name=(_('User Type')))
    # username=models.CharField(max_length=255,null=True,blank=True)
    tenant=models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True,)
    # role=models.ForeignKey("roles.Role",on_delete=models.SET_NULL,null=True, blank=True)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    registed_date=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['phone_number','user_type']

    objects=UserManagement() 
    class Meta:
        db_table='global_users'
        indexes=[
            models.Index(fields=['email']),
            models.Index(fields=["tenant"]),
            models.Index(fields=["phone_number"]),
            # models.Index(fields=["phone_number"]),
        ]
    def __str__(self):
        return f'{self.email}'
    
    def get_phone_number(self):
        return f"{self.phone_number}"
    
    def token(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
        
    def  save(self,*args,**kwargs):
        
        if self.user_type=='super_admin':
            self.is_superuser = True
            self.is_staff = True
            self.is_verified = True
            self.tenant=None
            self.tenant_role=None

        elif self.user_type =='paltform_staff':
            self.is_superuser = False
            self.is_staff = True
            self.tenant=None
            self.tenant_role=None
            # self.phone_number=None

        elif self.user_type =='tenant_admin':
            self.is_superuser = False
            self.is_staff = False
            # self.is_admin=True
            # self.is_verified = True
            if not self.tenant :
                 ValueError(f"Tenant user must have tenant")

        elif self.user_type=='tenant_member':
            self.is_superuser = False
            self.is_staff = False            
            if not self.tenant or not self.phone_number:
                ValueError("Tenant user must have tenant and  phone_number")
        super().save(*args,**kwargs)

class OneTimePassword(models.Model):
    user=models.OneToOneField(AccountUser,on_delete=models.Case)
    secret_key=models.CharField(max_length=64,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()

    def genarate_otp(self):
        totp=pyotp.TOTP(self.secret_key,interval=30)
        otp=totp.now()
        print(f"Generated OTP: {otp}, Secret: {self.secret_key}")
        return otp
    
    def verify_Otp(self,otp):
        totp=pyotp.TOTP(self.secret_key,interval=30)
        is_valid=totp.verify(otp,valid_window=3)
        return is_valid
    
    def is_expired(self):
       return timezone.now()>self.expires_at
    
    def save(self,*args, **kwargs):
        if not self.secret_key:
            self.secret_key=pyotp.random_base32()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_phone_number}-passcode"  