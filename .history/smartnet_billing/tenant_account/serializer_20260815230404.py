from rest_framework import serializers
from accounts.models import AccountUser
from .models import TenantUser,USER_STATUS
from branches.models import Branch
from roles.models import Role
class RegisterStaffSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255,required=False)
    username=serializers.CharField(max_length=255,required=False)
    phone_number=serializers.CharField(max_length=20,required=False)
    password=serializers.CharField(max_length=56,write_only=True)
    branch=serializers.CharField(max_length=225,required=False)
    role=serializers.CharField(max_length=225,required=False)
    status=serializers.ChoiceField(choices=USER_STATUS,required=False) 
    avatar=serializers.ImageField(required=False)

    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        return super().create(validated_data)
    
class ProfileDetailsSerializer(serializers.ModelSerializer):
    email=email=serializers.EmailField(source='global_user.email',read_only=True)
    phone_number=serializers.EmailField(source='global_user.phone_number',read_only=True)
    class Meta:
        model=TenantUser
        fields=['email','phone_number','username','avatar','address',]
