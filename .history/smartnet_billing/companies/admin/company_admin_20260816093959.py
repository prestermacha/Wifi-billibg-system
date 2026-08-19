from django.conf import settings
from django.contrib import admin
from django.db import connection
from companies.models import Company
from jazzmin.settings import get_settings

platform_name=getattr(settings,'PLATFORM_NAME','saas')

class TenantAdminSite(admin.AdminSite):
    site_header=f"{platform_name}Client Admin"
    site_title=f'{platform_name} Client Admin Portal'
    index_title='System Management'
 
    def has_permission(self, request):

        return request.user.is_active and request.user.is_staff 


    def each_context(self, request):
        context = super().each_context(request)
        # Force Jazzmin settings
        context.update(get_settings())
        
        if connection.schema_name != 'public':
            try:
                tenant = Company.objects.get(schema_name=connection.schema_name)
                context['site_header'] = f"{tenant.company_name} - Admin"
                context['site_title'] = tenant.company_name
                context['site_brand'] = tenant.company_name
            except:
                pass
        return context
    
    def has_module_permission(self,request,app_label):
        # return request.user.is_active and request.user.is_staff
        return request.user.is_active and request.user.is_staff
    