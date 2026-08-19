
from django.contrib import admin
from django.urls import path,include
from super_admin.admin.super_admin import super_admin_site
urlpatterns = [
    path('super-admin/', super_admin_site.urls),
    path('api/auth/',include('companies.urls')),
    # path('api/super-admin/',include('billing.urls')),
    # path('api/super-admin/',include('super_admin.urls'))
    
]
