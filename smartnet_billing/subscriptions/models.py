from django.db import models
from django.utils import timezone
import uuid
from companies.models import Company
# Create your models here.


STATUS_CHOICES = (
    ('trial', 'Trial'),
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('cancelled', 'Cancelled'),
)

INVOICE_STATUS=(
    ('pending','Panding'),
    ('paid','Paid'),
    ('overdue','Overdue'),
    ('sent','Sent'),
    ('draft','Draft'),
    ('cancelled','Cancelled'),
)

PAYMENT_STATUS=(
    ('pending','Panding'),
    ('paid','Paid'),
    ('failed','Failed'),
    ('refund','Refund'),
    ('cancelled','Cancelled')
)

PAYMENT_METHOD=(
    ('crdb','CRDB'),
    ('nmb','NMB'),
    ('m-pesa','M-pesa'),
    ('halo-pesa','Halo-pesa'),
    ('mix-by-yas','Mix-By-Yas'),
    ('airtel-money','Airtel-Money'),
)

REMINDER_TYPE_CHOICE=(
    ('sms','SMS'),
    ('email','Email'),
    ('both','Both'), 
)

STATUS_CHOICE=(
    ('pending','Panding'),
    ('sent','Sent'),
    ('failed','Failed'),
)


PACKAGE_CHOICES = (
        ('trial','Trial'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
)
BADGE_CHOICES=(
    ('popular',"Popular"),
    ('best_value','Best Value'),
)
DURATION_CHOICES = (
        (14,"14 days"),
        (1, "1 Month"),
        (2, "2 Months"),
        (3, "3 Months"),
        (6, "6 Months"),
        (12,"12 Months"),
)
class SubscriptionPlan(models.Model):
    name=models.CharField(max_length=100,unique=True,choices=PACKAGE_CHOICES)
    description=models.TextField(blank=True)
    features=models.JSONField(default=dict,null=True,blank=True)
    limit=models.JSONField(default=dict,blank=True,null=True)
    is_active=models.BooleanField(default=True)    
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} "

class PlanPricing(models.Model):
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,related_name='pricing')
    duration_months=models.PositiveBigIntegerField(choices=DURATION_CHOICES)
    badge=models.CharField(max_length=50,null=True,blank=True,choices=BADGE_CHOICES)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    is_active=models.BooleanField(default=True) 

    class Meta:
        unique_together = (
            "plan",
            "duration_months"
        )

    def __str__(self):
        return f'{self.plan.name}'


class TenantSubscription(models.Model):
    tenant=models.ForeignKey(Company,on_delete=models.CASCADE,)
    # plan=models.ForeignKey(SubscriptionPlan,on_delete=models.PROTECT)    
    pricing = models.ForeignKey(PlanPricing,on_delete=models.PROTECT)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='trial')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date=models.DateTimeField()   


    def __str__(self):
        return f"{self.tenant.company_name} - {self.pricing.plan.name}"
    
    def check_is_active(self):
        return (self.payment_status == 'paid' and self.end_date > timezone.now())
    
    def  days_remaining(self):
        if not self.status=='active':
            return 0
        delta=self.end_date - timezone.now()
        return max(0,delta.days)
    
    def has_expired(self):
        return( timezone.now() > self.end_date)
    
class Invoice(models.Model):
    tenant=models.ForeignKey(Company,on_delete=models.CASCADE)
    subcription=models.ForeignKey(TenantSubscription,on_delete=models.SET_NULL,null=True)
    invoice_number=models.CharField(max_length=20,unique=True)
    amount_due=models.DecimalField(decimal_places=2,max_digits=10)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid=models.BooleanField(default=False)
    status=models.CharField(max_length=20,choices=INVOICE_STATUS)
    payment_date=models.DateTimeField(blank=True,null=True)
    description=models.TextField(blank=True)
    notes=models.TextField(blank=True)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS,blank=True,null=True)
    payment_method=models.CharField(max_length=50,choices=PAYMENT_METHOD,blank=True,null=True)
    payment_referance=models.CharField(max_length=100,null=True,blank=True)


    def save(self,*args,**kwargs):
        if not self.invoice_number:
            self.invoice_number= f"INV-{uuid.uuid4().hex[:8].upper()}"
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return f"Invoice # {self.invoice_number} for {self.tenant}"
    
    def is_overdue(self):

        return (self.status not in ['paid','cancelled'] and self.due_date < timezone.now())
    

class Payment(models.Model):
    transaction_id=models.CharField(max_length=200,unique=True)
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='payments')
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    payment_method=models.CharField(max_length=50,choices=PAYMENT_METHOD,blank=True,null=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=PAYMENT_STATUS)

    def __str__(self):
        return f"{self.invoice.invoice_number}"


class PaymentReminder(models.Model):
    # transaction_id=models.CharField(max_length=10,unique=True)
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='reminder')
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    reminder_type=models.CharField(max_length=50,choices=REMINDER_TYPE_CHOICE,blank=True,null=True)
    scheduled_date = models.DateTimeField()
    sent_date =models.DateTimeField(null=True,blank=True)
    message=models.TextField()
    error_message=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.invoice.invoice_number}"










