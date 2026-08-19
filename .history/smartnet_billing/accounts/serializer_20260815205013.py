from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from companies.models import Domain
from django_tenants.utils import get_tenant_model, schema_context
from tenant_account.models import TenantUser

# class Registration(serializers.Serializer):

# class RegisterSerializer(serializers.Serializer):


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


