from django.shortcuts import render
from .serializer import CurrencySerializer
from .models import Currency
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.



class CurrencyView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CurrencySerializer
    queryset=Currency.objects.all()

    def get(self,request):
        queryset=self.get_queryset()
        serializer=CurrencySerializer(queryset,many=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)