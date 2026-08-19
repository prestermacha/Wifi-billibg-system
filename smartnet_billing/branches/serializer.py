from rest_framework import serializers
from .models import Branch,STATUS_CHOICES
from currency.models import Currency
from django.db import transaction


class BranchSerializer(serializers.Serializer):
    branch_id = serializers.CharField(read_only=True)
    branch_name = serializers.CharField(max_length=255, required=False)
    branch_address = serializers.CharField(max_length=255, required=False)
    # store_code=serializers.CharField(max_length=20, required=False)
    city=serializers.CharField(max_length=100, required=False)
    receipt_footer=serializers.CharField(max_length=255, required=False)
    default_status=serializers.ChoiceField(choices=STATUS_CHOICES,required=False)
    # tax_enabled=serializers.BooleanField(required=False)
    # allow_negative_stock=serializers.BooleanField(required=False)
    # show_mrp_on_invoice=serializers.BooleanField(required=False)
    # show_discount_tax_on_invoice=serializers.BooleanField(required=False)
    currency=serializers.PrimaryKeyRelatedField(
    queryset=Currency.objects.all(),required=False)
    timezone=serializers.CharField(max_length=100, required=False)
    # logo_image = serializers.ImageField(required=False)
    # signature_image = serializers.ImageField(required=False)
    phone_number = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField(max_length=255, required=False)
    bank_details = serializers.CharField(max_length=500, required=False)
    phone_onInvoice = serializers.BooleanField(required=False)
    email_onInvoice = serializers.BooleanField(required=False)


    def _get_company(self):
        """Single source of truth for the company from request context."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        company = request.user.tenant
        if not company:
            raise serializers.ValidationError("User must belong to a company.")
        return company

    def validate(self, attrs):
        branch_name = attrs.get('branch_name')
        company = self._get_company()

        # On create: check name uniqueness within THIS company only
        if branch_name:
            instance = self.instance  # None on create, set on update
            qs = Branch.objects.filter(branch_name=branch_name, company=company)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'branch_name': 'A Branch with this name already exists in your company.'}
                )
        return attrs

    def create(self, validated_data):
        company = self._get_company()  
        branch = Branch.objects.create(
            company=company,            
            **validated_data
        )
        return branch

    def update(self, instance, validated_data):
        # Prevent changing the company via update
        validated_data.pop('company', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BranchListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Branch
        fields=['branch_id','branch_name','email','phone_number','is_head_office' ,'currency','email_onInvoice','phone_onInvoice']


class BranchDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields='__all__'

