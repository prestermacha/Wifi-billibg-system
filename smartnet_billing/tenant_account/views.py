from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from  .models import TenantUser
from .serializer import ProfileDetailsSerializer
# Create your views here.

class ProfileDetailsView(GenericAPIView):
    serializer_class=ProfileDetailsSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return TenantUser.objects.get(global_user=user)

    def get(self,request):
        queryset=self.get_queryset()
        serializer=ProfileDetailsSerializer(queryset)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    # return Re


