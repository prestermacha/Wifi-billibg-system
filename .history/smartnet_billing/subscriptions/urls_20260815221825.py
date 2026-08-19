from django.urls import path
from .views import SubscriptionPlanView
urlpatterns=[
    path("subscription-plan/",SubscriptionPlanView.as_view(),name='subscription-plan'),
    path("subscription-plan/<int:id>/",SubscriptionPlanView.as_view(),name='subscription-plan'),
]