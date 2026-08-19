from django.contrib import admin
from branches.models import Branch
# Register your models here.

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display=['branch_id','branch_name','branch_address','email','phone_number','bank_details','slug','email_onInvoice','phone_onInvoice']
   