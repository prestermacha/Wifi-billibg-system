from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManagement(BaseUserManager):
    def email_validation(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise (_('Enter valid email address'))
        
    def create_user(self,email,phone_number,user_type,password=None,**extra_field):
        if email:
            email=self.normalize_email(email)
            self.email_validation(email)
        else:
            raise ValidationError(_('Email for user is required'))
        if not phone_number:
            raise ValidationError(_('Phone Number is required'))
        if not user_type:
            raise ValidationError(_('User Type is required'))
        

        user=self.model(email=email,phone_number=phone_number,user_type=user_type,**extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,phone_number,user_type,password=None,**extra_field):
        extra_field.setdefault('is_superuser',True)
        # extra_field.setdefault('is_admin',True)
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_verified',True)
        extra_field.setdefault('is_active',True)
        user_type='super_admin'

        if extra_field.get('is_superuser') is not  True:
            raise ValidationError(_('is_superuser for admin must be True'))
        if extra_field.get('is_staff') is not  True:
            raise ValidationError(_('is_staff for admin must be True'))    
        # if extra_field.get('is_admin') is not  True:
        #     raise ValidationError(_('is_admin for admin must be True'))
        if extra_field.get('is_active') is not  True:
            raise ValidationError(_('is_active for admin must be True'))
        if extra_field.get('is_verified') is not  True:
            raise ValidationError(_('is_verified for admin must be True'))
        
        user=self.create_user(email=email,phone_number=phone_number,user_type=user_type,password=password,**extra_field)
        user.save(using=self._db)
        return user
    
    def create_tenant_member(self,email,password,phone_number,user_type="tenant_member",**extra_field):
        user=self.create_user(email=email,phone_number=phone_number,user_type=user_type,password=password,**extra_field)  
        user.save(using=self._db)
        return user 
    
    def create_tenant_admin(self,email,password,phone_number,user_type,**extra_field):
        # extra_field.setdefault('is_superuser',False)
        # extra_field.setdefault('is_admin',True)
        # extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_verified',True)
        extra_field.setdefault('is_active',True)
        user_type='tenant_admin'
        
        # if extra_field.get('is_superuser') is not  False:
        #     raise ValidationError(_('is_superuser for admin must be True'))
        # if extra_field.get('is_staff') is not  True:
        #     raise ValidationError(_('is_staff for admin must be True'))    
        # if extra_field.get('is_admin') is not  True:
        #     raise ValidationError(_('is_admin for admin must be True'))
        if extra_field.get('is_active') is not  True:
            raise ValidationError(_('is_active for admin must be True'))
        if extra_field.get('is_verified') is not  True:
            raise ValidationError(_('is_verified for admin must be True'))
        user=self.create_user(email=email,phone_number=phone_number,user_type=user_type,password=password,**extra_field) 
        user.save(using=self._db)
        return user