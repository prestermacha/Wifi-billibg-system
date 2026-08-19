# from xml.etree.ElementTree import fromstring
from django.contrib import admin
from django.contrib.auth.models import Permission,Group
from companies.models import Company,Domain
from accounts.models import AccountUser
from django.contrib.auth.admin import UserAdmin
from subscriptions.models import SubscriptionPlan,TenantSubscription,Invoice,PaymentReminder,Payment,PlanPricing
from .admin import UserModelAdmin,CompanySuperAdmin,DomainSuperAdmin,SubcriptionPlanSuperAdmin,TenantSubcriptionSuperAdmin,InvoiceSuperAdmin,PaymentReminderSuperAdmin,PaymentSuperAdmin,PlanPricingAdmin,CurrencyAdmin
# from audit.models import AuditLog
from currency.models import Currency
class SuperAdminSite(admin.AdminSite):

    site_header="Super Admin"
    site_title='Super Admin Portal'
    index_title='System Management'

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser
        
     
    
    def index(self, request, extra_context = None):
        extra_context=extra_context or {}
        extra_context['company_count']=Company.objects.count()

        return super().index(request, extra_context)
    # def __init__(self, name = ...):
    #     super().__init__(name)
    #     # self.register(Domain)
    #     # self.register(Company)


super_admin_site=SuperAdminSite(name='super_admin_site')

class SUperAdminUserAdmin(UserAdmin):

    ordering=("email")
    list_display=[
        # 'username',
        'email',
        'phone_number',
        'user_type',
        'is_active',
        # 'is_admin',
        'is_verified',
        'is_staff',
        'role'
    ]
    list_filter=[
        'user_type',
        'is_active',
        # 'is_admin',
        'is_verified',
        'is_staff'
    ]
    search_fields=[
        # 'username',
        'email',
        'phone_number',
    ]

    def get_queryset(self, request):
        qs=super().get_queryset(request)
        if hasattr(request,'company') and request.company:
         return qs.filter(Company=request.company)
        return  qs  
    # def get_queryset(self, request):
    #     return super().get_queryset(request)


super_admin_site.register(AccountUser,UserModelAdmin)
super_admin_site.register(Company,CompanySuperAdmin)
super_admin_site.register(Domain,DomainSuperAdmin)
super_admin_site.register(SubscriptionPlan,SubcriptionPlanSuperAdmin)
super_admin_site.register(PlanPricing,PlanPricingAdmin)
super_admin_site.register(TenantSubscription,TenantSubcriptionSuperAdmin)
super_admin_site.register(Invoice,InvoiceSuperAdmin)
super_admin_site.register(Payment,PaymentSuperAdmin)
super_admin_site.register(PaymentReminder,PaymentReminderSuperAdmin)
# super_admin_site.register(AuditLog,AuditLogAdmin)
super_admin_site.register(Currency,CurrencyAdmin)

super_admin_site.register(Permission)
super_admin_site.register(Group)