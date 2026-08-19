from django.shortcuts import render
from .serializer import SubscriptionPlanSerializer,PlanPricingSerializer,SubscriptionListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import SubscriptionPlan,PlanPricing
from django.shortcuts import get_object_or_404
# from account.permission import ISSuperAdmin
import logging
# Create your views here.
logger=logging.getLogger(__name__)
class  SubscriptionPlanView(GenericAPIView):
    serializer_class=SubscriptionPlanSerializer
    permission_classes=[IsAuthenticated]
    # permission_classes=[ISSuperAdmin]

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        return SubscriptionPlan.objects.all()
    
    def get(self,request):
        queryset=self.get_queryset()
        serializer=SubscriptionPlanSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    lookup_field='id'
    def get_object(self):
        id=self.kwargs.get(self.lookup_field)
        return get_object_or_404(SubscriptionPlan,id=id)
    
    def patch(self,request,*agrs,**kwargs):
        subscription=self.get_object()
        serializer=self.serializer_class(subscription,partial=True,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,*agrs,**kwargs):
        subscription=self.get_object()
        serializer=self.serializer_class(subscription,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*agrs,**kwargs):
        subscription=self.get_object()
        # if isinstance(subscription,Response):
        subscription.delete()
        return Response({"message": "Subscriptional deleted successfully"},status=status.HTTP_200_OK,)



class PlanPricingView(GenericAPIView):
    serializer_class=PlanPricingSerializer
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PricingPlanListView(GenericAPIView):
    serializer_class=SubscriptionListSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return SubscriptionPlan.objects.filter(is_active=True).prefetch_related('pricing')

    def get(self,request):
        queryset=self.get_queryset()
        serializer=SubscriptionListSerializer(queryset,many=True)
        logger.info(serializer.data)
        # logger.info(f'plan {serializer.data['plan']}')
        return Response(serializer.data,status=status.HTTP_200_OK)
    





