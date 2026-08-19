from django.urls import path
# from company.views import CompanyDetails
from tenant_account.views import ProfileDetailsView

urlpatterns=[
        # path('company-detals/',CompanyDetails.as_view(),name='company-detals'),
        path('profile-details/',ProfileDetailsView.as_view(),name='profile-details'),
]