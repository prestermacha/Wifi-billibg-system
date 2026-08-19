from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from company.models import Company
from .models import SubscriptionPlan,TenantSubscription,PlanPricing
from django.db.models.signals import post_save

# registration signal 
@receiver(post_save, sender=Company)
def create_trial_subscription(sender,instance,created,**kwargs):

    if created:
        # if instance.package=='basic':
            # basic_plan=SubscriptionPlan.objects.get(name='Basic')
            trial_plan=PlanPricing.objects.get(
                  id=1,
                  duration_months=14,
            )
            TenantSubscription.objects.create(
                tenant=instance,
                pricing=trial_plan,
                start_date=timezone.now(),
                payment_status='pending',
                end_date=timezone.now()+timedelta(days=14),
                status='trial'
            )
        # if instance.package=='standard':
        #     standard_plan=SubscriptionPlan.objects.get(name='Standard')
        #     TenantSubcription.objects.create(
        #         tenant=instance,
        #         plan=standard_plan,
        #         start_date=timezone.now(),
        #         payment_status='paid',
        #         end_date=timezone.now()+timedelta(days=30),
        #         status='active'
        #     )

        # if instance.package=='pro':
        #     pro_plan=SubscriptionPlan.objects.get(name='pro')
        #     TenantSubcription.objects.create(
        #         tenant=instance,
        #         plan=pro_plan,
        #         start_date=timezone.now(),
        #         payment_status='paid',
        #         end_date=timezone.now()+timedelta(days=30),
        #         status='active'
        #     )
            
        # if instance.package=='enterprise':
        #     enterprise_plan=SubscriptionPlan.objects.get(name='enterprise')
        #     TenantSubcription.objects.create(
        #         tenant=instance,
        #         plan=enterprise_plan,
        #         start_date=timezone.now(),
        #         payment_status='paid',
        #         end_date=timezone.now()+timedelta(days=30),
        #         status='active'
        #     )

# remeinder subscriptional message
