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
        
    def create_user(self,email,phone_number,user_type,username,password=None,**extra_field):
        if email:
            email=self.normalize_email(email)
            self.email_validation(email)
        else:
            raise ValidationError(_('Email for user is required'))
        if not phone_number:
            raise ValidationError(_('Phone Number is required'))
        if not user_type:
            raise ValidationError(_('User Type is required'))
        