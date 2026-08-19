from django.core.management import BaseCommand
from django.utils import timezone
from ...models import TenantSubscription,Invoice
from datetime import timedelta

class Command(BaseCommand):
    help= "Invoice Generation"

    def handle(self, *args, **kwargs):

        subscriptions = TenantSubscription.objects.filter(
            status='active'
        )

        for sub in subscriptions:

            Invoice.objects.create(
                tenant=sub.tenant,
                subcription=sub,
                amount_due=sub.plan.price,
                due_date=timezone.now() + timedelta(days=7),
                status='pending'
            )

        self.stdout.write("Invoices generated")
    



