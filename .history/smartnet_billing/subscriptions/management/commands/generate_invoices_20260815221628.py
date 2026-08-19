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
    


# class Invoice(models.Model):
#     tenant=models.ForeignKey(Company,on_delete=models.CASCADE)
#     subcription=models.ForeignKey(TenantSubcription,on_delete=models.SET_NULL,null=True)
#     invoice_number=models.CharField(max_length=20,unique=True)
#     amount_due=models.DecimalField(decimal_places=2,max_digits=10)
#     issue_date = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField()
#     is_paid=models.BooleanField(default=False)
#     status=models.CharField(max_length=20,choices=INVOICE_STATUS)
#     payment_date=models.DateTimeField(blank=True,null=True)
#     description=models.TextField(blank=True)
#     notes=models.TextField(blank=True)
#     payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS,blank=True,null=True)
#     payment_method=models.CharField(max_length=50,choices=PAYMENT_METHOD,blank=True,null=True)
#     payment_referance=models.CharField(max_length=100,null=True,blank=True)
