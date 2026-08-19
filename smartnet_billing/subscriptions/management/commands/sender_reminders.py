from django.core.management import BaseCommand
from django.utils import timezone
from ...models import TenantSubscription

class Command(BaseCommand):
    help= "Send Expiry Reminders"

    def handle(self, *args, **options):
        upcoming=TenantSubscription.objects.filter(
            status='active',
            end_date=timezone.now()
        )
        # count=expired.update(status='expired')
        for sub in upcoming:
            print(f"send reminder to {sub.tenant}")
        # return super().handle(*args, **options)
    
    
