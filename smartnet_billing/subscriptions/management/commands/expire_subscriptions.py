from django.core.management import BaseCommand
from django.utils import timezone
from ...models import TenantSubscription

class Command(BaseCommand):
    help= "Expire Subscription"

    def handle(self, *args, **options):
        expired=TenantSubscription.objects.filter(
            status='active',
            end_date=timezone.now()
        )
        count=expired.update(status='expired')
        self.stdout.write(
            self.style.SUCCESS(f"{count} subscriptions expired")
        )
        # return super().handle(*args, **options)
    
    
