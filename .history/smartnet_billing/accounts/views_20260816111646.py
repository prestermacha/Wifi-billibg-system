from django.shortcuts import render
from .serializer import LoginSerializer
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.sendemail import send_otp_to_user,resend_code_to_user
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializer import LoginSerializer,RegisterSerializer,VerifyEmailSerializer,ResendOtpSerializer
from accounts.models import AccountUser,OneTimePassword
from companies.models import Company
# Create your views here.
class RegistrationView(GenericAPIView):
    serializer_class=RegisterSerializer
    authentication_classes = []
    permission_classes=[AllowAny]
     
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            send_otp_to_user(user.email)
            company = Company.objects.filter(owner=user).latest('created_at')
            short_id = company.company_id.hex[:8]
            domain_name = f"{short_id}.localhost"
            refresh = RefreshToken.for_user(user)

            response_data = {
            'email': user.email,
            'phone_number': user.phone_number,
            'company_name': company.company_name,
            'company_id': str(company.company_id),
            'user_type': user.user_type,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'is_active': company.is_active,
            'domain': domain_name,
        }
            
            # print(serializer.data)
            # logger.info(f' login user is as follow {user}')
            return Response(response_data,status=status.HTTP_201_CREATED)
        # print(serializer.error)
        # logger.info(f' login user is as follow {user}')
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            data=serializer.validated_data
            user=data.pop('user')
            refresh=RefreshToken.for_user(user)
            access_token=str(refresh.access_token)
            refresh_token=str(refresh)

            response=Response(data,status=status.HTTP_200_OK)

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                domain='.lvh.me',
                max_age=60*15
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                domain='.lvh.me',
                max_age=60*60*24*7
            )
            return  response 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(GenericAPIView):
    serializer_class=VerifyEmailSerializer
    permission_classes=[AllowAny]
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp_code=serializer.validated_data['totp']
            email=serializer.validated_data['email'] 
            print(f"Validated OTP: {otp_code}, Email: {email}")
            try:
                user=AccountUser.objects.get(email=email)
                user_code=OneTimePassword.objects.filter(user=user).latest('created_at')
                print(f"Submitted OTP: {otp_code}, Secret: {user_code.secret_key}")

                if user_code.is_expired():
                    print("OTP is expired")
                    user_code.delete()
                    return Response({'message': 'OTP expired'},status=status.HTTP_400_BAD_REQUEST )
                 
                print(f"Calling verify_Otp with OTP: {otp_code}")
                is_valid = user_code.verify_Otp(otp_code)
                print(f"verify_Otp result: {is_valid}")

                if is_valid:
                    print("OTP verified successfully")
                    user_code.delete()
                    if not user.is_verified:
                        user.is_verified = True
                        user.save()
                        print("User verified and saved") 
                        # send_login_notification(user=user)
                        return Response({'message': 'Account email verified successfully'}, status=status.HTTP_200_OK)
                    print("User already verified")
                   
                    return Response({'message': 'User already verified'},status=status.HTTP_200_OK)
                return Response({'message': 'Invalid OTP code'},status=status.HTTP_400_BAD_REQUEST)
            except AccountUser.DoesNotExist:
                  return Response({'message': 'User with this email does not exist'},status=status.HTTP_404_NOT_FOUND)
            except OneTimePassword.DoesNotExist:
                   return Response({'message': 'No valid OTP found for this user'}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
class ResendOtpView(GenericAPIView):
    serializer_class=ResendOtpSerializer
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            try:
                resend_code_to_user(email)
                # logging.info(f"OTp send to the {email}")
                return Response({"message": f"New OTP sent to your {email}."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send OTP: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        # print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



