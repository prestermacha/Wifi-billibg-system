from rest_framework import serializers
from .models import Role

class RolesList(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['id','name','description','is_system']


