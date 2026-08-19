from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken,AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # print("HOST:", request.get_host())
        # print("COOKIES:", request.COOKIES)

        token = request.COOKIES.get("access_token")

        print("TOKEN:", token)
        # try cookies 
        raw_token=request.COOKIES.get(settings.SIMPLE_JWT.get("AUTH_COOKIE", "access_token"))

        # fall back to authorization header
        if raw_token is None:
            header=self.get_header(request)
            if header is not None:
              raw_token= self.get_raw_token(header)
        
        if raw_token is None:
            return None
        
        
        
        try:
           validate_token=self.get_validated_token(raw_token)
        except InvalidToken as e:
            raise AuthenticationFailed(str(e))
        
        user=self.get_user(validate_token)

        return (user,validate_token)
        
        # return super().authenticate(request)