from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from companies.models import Domain,Company
from django_tenants.utils import get_tenant_model, schema_context,get_public_schema_name
from tenant_account.models import TenantUser
from django.contrib.auth.password_validation import validate_password
from accounts.models import AccountUser
from currency.models import Currency
from permissions.models import CustomPermission
from roles.models import Role
from django.db import transaction
from branches.models import Branch
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255,)
    phone_number=serializers.CharField(max_length=25,)    
    company_name=serializers.CharField(max_length=250)
    company_id=serializers.CharField(max_length=25,read_only=True)   
    password= serializers.CharField(max_length=60,write_only=True)
    password2= serializers.CharField(max_length=60,write_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)
    is_active=serializers.BooleanField(read_only=True)


    def validate(self, attrs):
        password=attrs.get('password', '')    
        password2=attrs.get('password2', '')  
        validate_password(password)
        if password!=password2:
           raise serializers.ValidationError("password do n't match")
        email=attrs.get('email')
        if AccountUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": f"User  already exists in the system with this {email}"})
        return super().validate(attrs)

    
    @transaction.atomic
    def create(self, validated_data):
        # 1. create platform owner
        user=AccountUser.objects.create(
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            user_type='tenant_admin',
            # phone_number=validated_data.get('')
        )
        user.set_password(validated_data['password'])
        user.save()
        # RefreshToken.for_user(user)

        # 2.Create company & domain in public schema
        with schema_context(get_public_schema_name()):
            company=Company.objects.create(
                owner=user,
                company_name=validated_data.get('company_name'),
                email=validated_data['email'],
                phone=validated_data.get('phone_number'),
                is_active=True,
            )
           
            short_id = company.company_id.hex[:8]  
            # domain_name = f"{short_id}.localhost"  
            domain_name = f"{short_id}.lvh.me"
            
 
            Domain.objects.create(
                domain=domain_name,
                tenant=company,
                is_primary=True
            )
            company.save()
            # domain.save()
            
            user.tenant=company
            user.save()
             
        with schema_context(company.schema_name):
            currency=Currency.objects.get(currency_code='TZS')
            branch=Branch.objects.create(
              store_name=f'{company}-Store',
              company=company,
              currency=currency,
              email=validated_data['email'],
              phone_number=validated_data.get('phone_number'),
              is_head_office=True,
            )
            branch.save()
            admin_role=Role.objects.create(
                company=company,
                name="Admin",
                slug="admin",
                is_system =True
            )
            admin_role.permissions.set(
                CustomPermission.objects.all()
            )
            TenantUser.objects.create(
                    global_user=user,
                    username="Admin",
                    role=admin_role,
                    status='enabled',
                    
                )
            # tenant_user.save()
        return user
 
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    paswrd=serializers.CharField(max_length=56,write_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)
    subdomain = serializers.CharField(max_length=50, read_only=True)  
    company_name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')

        user=authenticate(request=request,email=email,password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        
        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")
        
        subdomain = None
        company_name = None

        # =====================================================
        # PLATFORM USERS
        # =====================================================
        if user.user_type in ["super_admin","paltform_staff"]:
             return {
                "user": user,
                # "access_token": access_token,
                # "refresh_token": refresh_token,
                "subdomain": "platform",
                "company_name": "Platform",
                # "role": user.user_type,
                # "permissions": ["all"],
                "user_type": user.user_type,
            }
        
        company=user.tenant

        if not company:
            raise AuthenticationFailed("No company associated with this account")
        
        # GET DOMAIN
        domain = Domain.objects.filter(tenant=company,is_primary=True).first()

        if domain:
            subdomain = domain.domain.split(".")[0]
        else:
            subdomain = company.schema_name

        company_name = company.company_name
        # =====================================================
        # SWITCH TO TENANT SCHEMA
        # =====================================================

        with schema_context(company.schema_name):

            tenant_user = TenantUser.objects.select_related("role").filter(global_user=user).first()

            if not tenant_user:
                raise AuthenticationFailed("Tenant profile not found")

            # ROLE
            if tenant_user.role:
                role_name = tenant_user.role.name
                # PERMISSIONS
                permissions = list(
                    tenant_user.role.permissions.values_list("codename",flat=True))
        return {
            "user": user,
            # "access_token": access_token,
            # "refresh_token": refresh_token,
            "subdomain": subdomain,
            "company_name": company_name,
            "role": role_name,
            "permissions": permissions,
            "user_type": user.user_type,
        }

class VerifyEmailSerializer(serializers.Serializer):
    totp=serializers.CharField(max_length=64)  
    email=serializers.EmailField(max_length=255)

    def validate_totp(self, attrs):
        if not attrs.isdigit() or  len(attrs)!=6:
            raise serializers.ValidationError({'error':'OTP must be a 6-digit number'})
        return attrs
    
    def validate_email(self, attrs):
        if not AccountUser.objects.filter(email=attrs).exists():
            raise serializers.ValidationError({'error':f'User with this {attrs} does not exist'})
        return attrs

class ResendOtpSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255,required=True)
    def validate_email(self, attrs):
        if not AccountUser.objects.filter(email=attrs).exists():
            raise serializers.ValidationError({'error':f'User with this {attrs} does not exist'})
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    default_error_messages={
      'bad_token':('Token is Invalid or has expired')
    }
    def validate(self,attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:    
             return self.fail('bad_token')
   

