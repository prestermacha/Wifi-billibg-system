from django.db import models,transaction,connection
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import connection
# from .permissions.role_permission import ROLE_PERMISSIONS
from django.apps import apps
from django.contrib.auth.models import BaseUserManager

User= get_user_model()

class TenantUserManager(BaseUserManager):
    def email_validation(self,email):
        try: 
            validate_email(email)
        except ValidationError   :
            raise(_('Enter a valid email address'))
           
    def create_tenant_user(self,global_user,email,username,phone_number,user_type,password=None,**extra_field):
        tenant_id=self.get_current_tenant_id()
        if email:
            email=self.normalize_email(email)
            self.email_validation(email)
        else:
            raise ValidationError(_('Email for user is required'))
        if not username:
            raise ValidationError(_('Username is required'))
        if not phone_number:
            raise ValidationError(_('Phone Number is required'))
        if not user_type:
            raise ValidationError(_('User Type is required'))
        
        global_user=self._get_or_create_global_user(
            email=email,
            # username=username,
            password=password,
            tenant_id=tenant_id,
            phone_number=phone_number,
            user_type=user_type,
            **extra_field
        )
         
        tenant_user=self.model(
            global_user=global_user,
            email=email,
            # staff_id=staff_id,
            username=username,
            # password=password,
            phone_number=phone_number,
            user_type=user_type,
            **extra_field
        )
        # tenant_user.set_password(password)
        tenant_user.save(using=self._db)
        # self._assign_permissions(tenant_user)
        return tenant_user
    
    def _get_or_create_global_user(self,global_user,email,tenant_id,phone_number,user_type,password=None,**extra_field):
        """
        Robust globleUser creation with multiple strategies handle duplicate
        """
        # check user exist
        try:
            global_user=User.objects.get(
                email=email,
                schema_name=tenant_id,
            )
            return global_user
        except User.DoesNotExist:
            pass

        # try to get email and update info 

        try:
            global_user=User.objects.get(email=email)
            global_user.phone_number=phone_number
            global_user.set_password(password)
            global_user.tenant_id=tenant_id

            if user_type in ["tenant_admin","branch_manager","market_officer"]:
                global_user.user_type="tenant_admin"
                global_user.tenant_role=user_type
            else:
                global_user.user_type="tenant_member"
            global_user.save()
            return global_user
        except User.DoesNotExist:
            if user_type in ["tenant_admin","branch_manager","market_officer"]:
                return User.objects.create_tenant_admin(
                    email=self.email,
                    phone_number=self.phone_number,
                    user_type='tenant_admin',
                    password=password
                )
            elif user_type=='member':
                return User.objects.create_tenant_member(
                    email=self.email,
                    phone_number=self.phone_number,
                    user_type='tenant_member',
                    password=password
                )

    def get_current_tenant_id(self):
         return connection.schema_name
    
    # def  _assign_permissions(self,tenant_user):

    #     if not tenant_user.global_user:
    #         return 
        
    #     global_user=tenant_user.global_user
    #     role=tenant_user.user_type
    #     role_config=ROLE_PERMISSIONS.get(role)
    #     if not role_config:
    #         return
        
    #     permissions_to_assign=set()

    #     apps=role_config.get('apps',[])
    #     actions=role_config.get('action',[])

    #     for app_label in apps:
    #         for action in actions:
    #             codename = f"{action}_{app_label}"
    #             permissions_to_assign.add((app_label, codename))

    #     custom_perms = role_config.get("custome_perms", [])
    #     for full_codename in custom_perms:
    #         if '.' in full_codename:
    #             app_label, codename = full_codename.split('.', 1)
    #             permissions_to_assign.add((app_label, codename))
    #         else:
    #             # If only codename is provided, assume it's in one of the allowed apps
    #             # Or you can skip/warn — better to enforce full app.codename
    #             continue
    #     permission_objects = []
    #     for app_label, codename in permissions_to_assign:
    #         try:
    #             permission = Permission.objects.get(
    #                 content_type__app_label=app_label,
    #                 codename=codename
    #             )
    #             permission_objects.append(permission)
    #         except Permission.DoesNotExist:
    #             # Optional: log this in production
    #             print(f"Warning: Permission '{app_label}.{codename}' does not exist.")
    #     if permission_objects:
    #         global_user.user_permissions.set(permission_objects)
            
    #     global_user.is_staff = role_config.get("is_staff", False)
    #     global_user.is_superuser = role_config.get("is_superuser", False)
    #     global_user.save(update_fields=['is_staff', 'is_superuser'])

    @transaction.atomic
    def create_owner(self,email,username,phone_number,user_type="tenant_admin",password=None,**extra_field):
        return self.create_tenant_user(email=email,username=username,phone_number=phone_number,user_type=user_type,password=password,**extra_field)
    
    @transaction.atomic
    def create_branch_manager(self,email,username,phone_number,user_type="branch_manager",password=None,**extra_field):
        return self.create_tenant_user(email=email,username=username,phone_number=phone_number,user_type=user_type,password=password,**extra_field)
    
    @transaction.atomic
    def create_market_officer(self,email,username,phone_number,password,user_type="market_officer",**extra_field):
        return self.create_tenant_user(email=email,username=username,phone_number=phone_number,user_type=user_type,password=password,**extra_field)
    
    @transaction.atomic
    def create_member(self,email,username,phone_number,user_type="member",password=None,**extra_field):
        return self.create_tenant_user(email=email,username=username,phone_number=phone_number,user_type=user_type,password=password,**extra_field)
        