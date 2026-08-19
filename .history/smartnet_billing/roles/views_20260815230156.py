from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView,DestroyAPIView
from rest_framework import status
from .serializer import RolesList
from .models import Role
# Create your views here.

class RoleListView(GenericAPIView):
    serializer_class=RolesList
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()

    def get(self,request):
        queryset=self.get_queryset()
        serializer=RolesList(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


