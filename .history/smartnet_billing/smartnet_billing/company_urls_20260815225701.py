from django.contrib import admin
from django.urls import path,include
# from company_admin.admin.company_admin import company_admin_site


urlpatterns = [
    # path('company-admin/',company_admin_site.urls,),
    path('branch/',include('branches.urls')),
    path('role/',include('roles.urls')),
    # path('brand/',include('brand.urls')),
    # path('category/',include('cartegory.urls')),
    path('currency/',include('currency.urls')),
    # path('purchase/',include('purchases.urls')),
    # path('supplier/',include('supplier.urls')),
    # path('customer/',include('customer.urls')),
    # path('admin/',include('company_admin.urls')),
    path('tenant-user/',include('tenant_account.urls')),
    # path('unit/',include('unit.urls')),
    # path('taxes/',include('taxes.urls')),
    # path('product/',include('products.urls')),
    # path('inventory/',include('inventory.urls')),


]
