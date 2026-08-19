from django.contrib import admin
from  companies.models import Company,Domain
from accounts.models import AccountUser
from subscriptions.models import Payment,TenantSubscription,PaymentReminder,SubscriptionPlan,Invoice,PlanPricing
# from audit.models import AuditLog
from currency.models import Currency
# Register your models here.

@admin.register(Company)
class CompanySuperAdmin(admin.ModelAdmin):
    list_display=[
        'company_id',
        'company_name',
        'owner',
        'address',
        'email',
        'phone',
        'is_active',
        # 'package',
        # 'subcription_plan',
        # 'trial_start_date',
        # 'trial_end_date'
        ]
@admin.register(Domain)
class DomainSuperAdmin(admin.ModelAdmin):
    list_display=['domain','tenant','is_primary']

@admin.register(AccountUser)  
class UserModelAdmin(admin.ModelAdmin):
    list_display=[
        # 'username',
        'email',
        'phone_number',
        'user_type',
        'is_active',
        'tenant',
        'is_verified',
        'is_staff',
        # 'role'
    ]
@admin.register(Payment)
class PaymentSuperAdmin(admin.ModelAdmin):
    list_display=[
        'transaction_id',
        'invoice',
        'amount',
        'payment_method',
        'status',
        'paid_at',
    ]

@admin.register(TenantSubscription)
class TenantSubcriptionSuperAdmin(admin.ModelAdmin):
    list_display=['tenant','pricing','payment_status','start_date','end_date','days_remaining']

@admin.register(PaymentReminder)
class PaymentReminderSuperAdmin(admin.ModelAdmin):
    list_display=['invoice','amount','reminder_type','scheduled_date','sent_date','message','error_message','status','created_at']

@admin.register(SubscriptionPlan)
class SubcriptionPlanSuperAdmin(admin.ModelAdmin):
    list_display=['id','name','description','features','is_active','create_at']


@admin.register(PlanPricing)
class PlanPricingAdmin(admin.ModelAdmin):
    list_display=['id','plan','duration_months','price','is_active']


@admin.register(Invoice)
class InvoiceSuperAdmin(admin.ModelAdmin):
    list_display=['tenant','subcription','invoice_number','amount_due','issue_date','due_date','is_paid','status','payment_date','payment_method','description','notes','payment_status','payment_referance']

    # def has_add_permission(self, request):
    #     return False

# @admin.register(AuditLog)
# class AuditLogAdmin(admin.ModelAdmin):
#     list_display=['tenant','user','action','level','resource','resource_id','description','ip_address','user_agent','metadata','created_at']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display=['name','symbol','position','currency_code']