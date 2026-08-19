from rest_framework import serializers
from .models import SubscriptionPlan,Payment,PAYMENT_METHOD,PAYMENT_STATUS,PlanPricing,DURATION_CHOICES,BADGE_CHOICES
from django.db import transaction
from django.utils import timezone



class SubscriptionPlanSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField(max_length=100,required=False)
    description=serializers.CharField(required=False)
    features=serializers.JSONField(required=False)
    limit=serializers.JSONField(required=False)
    is_active=serializers.BooleanField(required=False)    
    # durations=serializers.CharField(max)

    def validate(self, attrs):
        name=attrs.get('name')
        # duration_day=attrs('duration_day')
        if SubscriptionPlan.objects.filter(name=name).exists():
            raise serializers.ValidationError({"plan": f"Subscription Plan   already exists in the system with this {name}"})
        return attrs
    
    def create(self, validated_data):
        with transaction.atomic():
            plan=SubscriptionPlan.objects.create(
                name=validated_data.get("name"),
                description=validated_data.get("description"),
                features=validated_data.get("features"),
                limit=validated_data.get('limit'),
                is_active=validated_data.get("is_active"),
            )
            plan.save()
        return plan
    
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.features=validated_data.get('features',instance.features)
        instance.limit=validated_data.get('limit',instance.limit)
        instance.is_active=validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance

class PlanPricingSerializer(serializers.ModelSerializer):
    id=serializers.CharField(max_length=200,required=False)
    duration_months=serializers.ChoiceField(DURATION_CHOICES,required=False)
    price=serializers.DecimalField(decimal_places=2,max_digits=10) 
    badge=serializers.ChoiceField(BADGE_CHOICES,required=False)
    is_active=serializers.BooleanField(required=False) 
    savings=serializers.SerializerMethodField()
    class Meta:
        model = PlanPricing
        fields = ["id","duration_months","price",'is_active','badge','savings',]

    
    def get_savings(self,obj):
        monthly=obj.plan.pricing.filter(
            duration_months=1
        ).first()
        if not monthly:
            return 0
        expected=monthly.price * obj.duration_months

        return expected - obj.price

    def validate(self, attrs):
        id=attrs.get('id')
        try:
            plan=SubscriptionPlan.objects.get(id=id)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError('Subscription do not exist')
        self.plan=plan
        return attrs
    
    def create(self, validated_data):
        plan=self.plan
        with transaction.atomic():
            pricing=PlanPricing.objects.create(
                plan=plan,
                duration_months=validated_data.get('duration_months'),
                price=validated_data.get('price'),
                badge=validated_data.get('badge'),
                is_active=validated_data.get('is_active')
            )
            pricing.save()
        return  pricing
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class SubscriptionListSerializer(serializers.ModelSerializer):
    duration=PlanPricingSerializer(source='pricing',many=True)
    features=serializers.JSONField()
    limit=serializers.JSONField()
    tenant_count = serializers.SerializerMethodField()
    duration_count = serializers.SerializerMethodField()
    starting_price = serializers.SerializerMethodField()

    class Meta:
        model=SubscriptionPlan
        fields=['id','name','description','limit','features','is_active','duration_count','tenant_count','duration','starting_price']

    def get_duration_count(self, obj):
        return obj.pricing.count()

    def get_starting_price(self, obj):
        lowest = obj.pricing.order_by("price").first()
        return lowest.price if lowest else 0

    def get_tenant_count(self, obj):
        return (
            obj.pricing.filter(
                tenantsubscription__status="active"
            )
            .values("tenantsubscription__tenant")
            .distinct()
            .count()
        )




