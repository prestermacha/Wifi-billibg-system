from django.urls import path
from .views import RegistrationView,VerifyEmailView,ResendOtpView,LoginUserView
# CompanyDetails,LogoutView,RefreshTokenView,PasswordResetRequestView,PasswordResetConfirm,SetNewPassword

urlpatterns=[
    path('register/',RegistrationView.as_view(),name='register-company'),  
    path('login/',LoginUserView.as_view(),name='login'),
    # path("token/refresh/",RefreshTokenView.as_view(),name='refresh-token'),
    path('verify-email/',VerifyEmailView.as_view(),name='verify-email'),
    path('resend-otp/',ResendOtpView.as_view(),name='resend-otp'),
    # path('logout/',LogoutView.as_view(),name='logout'),
    # path('password-reset/',PasswordResetRequestView.as_view(),name='password-reset'),
    # path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirm.as_view(),name='password-reset-confirm'),
    # path('set-new-password/',SetNewPassword.as_view(),name='set-new-password'),



]