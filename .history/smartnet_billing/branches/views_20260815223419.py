from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework .generics import GenericAPIView,UpdateAPIView,DestroyAPIView
from .serializer import BranchSerializer,BranchDetailsSerializer,BranchListSerializer
from .models import Branch
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# Create your views here.

# store/views.py
from django.db import connection
from rest_framework.exceptions import PermissionDenied

class TenantPermissionMixin:
    """
    Mixin that ensures the authenticated user belongs to 
    the current request's tenant schema.
    """
    def get_current_schema(self):
        return connection.schema_name

    def validate_tenant_access(self):
        user = self.request.user
        company = getattr(user, 'tenant', None)

        if not company:
            raise PermissionDenied("No company associated with your account.")

        current_schema = self.get_current_schema()

        # Public schema access guard
        if current_schema == 'public':
            raise PermissionDenied("Cannot perform store operations in public schema.")

        # THE KEY CHECK: does the user's company match the current schema?
        if company.schema_name != current_schema:
            raise PermissionDenied(
                "You do not have access to this tenant."
            )

        return company  # safe to use
class BranchConfigView(TenantPermissionMixin,GenericAPIView):
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request):
        if not request.user.tenant:
            raise PermissionDenied("You must belong to a company to create Branch.")
        serializer=self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BranchListView(TenantPermissionMixin,GenericAPIView): 
    serializer_class=BranchListSerializer
    permission_classes=[IsAuthenticated]
    # queryset=Store.objects.all()
    
    def get_queryset(self):
        user=self.request.user
        if not user.tenant:
            return Branch.objects.none()
        return  Branch.objects.filter(company=user.tenant)
        return Store.objects.for_request(self.request)
    
    def get(self,request):
        queryset=self.get_queryset()
        serializer=BranchListSerializer(queryset,many=True)
        # print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class BranchDetailsView(TenantPermissionMixin,GenericAPIView):
    serializer_class=BranchDetailsSerializer
    permission_classes=[IsAuthenticated]
    lookup_field='branch_id'

    def get_queryset(self,):
        id=self.kwargs.get(self.lookup_field)
        return Branch.objects.get(branch_id=id)
    
    def get(self,request,*agrs,**kwargs):
        queryset=self.get_queryset()
        serializer=BranchDetailsSerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)
class BranchUpdateView(TenantPermissionMixin,GenericAPIView):
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticated]
    lookup_field='branch_id'

    def get_object(self):
        id = self.kwargs.get(self.lookup_field)
        return get_object_or_404(Branch,branch_id=id)
    

    def patch(self, request,*args,**kwargs): 
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Branch updated successfully!"}, status=status.HTTP_200_OK)
        # print("=============== data  request ==========================")
        # # print(request.data)
        # print("=========================================")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteBranch(DestroyAPIView):
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticated]
    lookup_field = 'branch_id'


    def get_object(self):
        id=self.kwargs.get(self.lookup_field)
        return get_object_or_404(Branch,branch_id=id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Branch deleted successfully"},
            status=status.HTTP_200_OK
        )


