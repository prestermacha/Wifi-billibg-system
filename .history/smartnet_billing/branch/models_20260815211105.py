from django.db import models, transaction
from base.models import BaseEntity,TenantManager,SoftDeleteModel
import uuid
from companies.models import Company
from django.utils.text import slugify
from django.core.validators import RegexValidator
from currency.models import Currency


# Create your models here.
def  user_directory_path(instance,filename):
    ext= filename.split(".")[-1]
    filename= "%s_%s" % (instance.id,ext)
    return "user_{0}/{1}".format(instance.store_name.id,filename)

phone_regex = RegexValidator(
    regex=r'^\+[1-9]\d{1,14}$',
    message='Phone number must be in E.164 format.'
    ) 

STATUS_CHOICES=(
    ('delivary','Delivary'),
    ('shipping','Shipping'),
    ('ordered','Ordered'),
    ('confirmed','Confirmed'),
    ('processing','Processing'),
    # ('shipping','Shipping'),
)

class Branch(BaseEntity,SoftDeleteModel):
    branch_id=models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False,)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name="stores")
    email=models.EmailField(max_length=255,)
    phone_number=models.CharField(max_length=20,validators=[phone_regex])
    bank_details=models.TextField(blank=True,null=True)
    branch_name = models.CharField(max_length=255,)
    branch_code = models.CharField(max_length=20,)
    city = models.CharField(max_length=100,blank=True,null=True)
    # allow_negative_stock = models.BooleanField(default=False)
    receipt_footer = models.TextField(blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True,)
    branch_address=models.CharField(max_length=100,blank=True,null=True)
    is_head_office = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency,on_delete=models.PROTECT,null=True, blank=True)
    timezone = models.CharField(max_length=100,blank=True,null=True)
    email_onInvoice=models.BooleanField(default=False)
    phone_onInvoice=models.BooleanField(default=False)

    class Meta:
        unique_together=(("company","branch_name",),("company", "branch_code"))
        indexes=[
            models.Index(fields=['company']),
            models.Index(fields=['slug'])
        ]
    
    objects =TenantManager()


    @classmethod
    def generate_branch_code(cls):
        with transaction.atomic():
            last_branch = (
                cls.objects.select_for_update()
                .order_by('-created_at')
                .first()
            )

            if not last_branch:
                return "BR0001"

            try:
                number = int(last_branch.store_code.replace("BR", ""))
            except:
                number = 0

            return f"STR{number + 1:04d}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.company.company_name}-{self.branch_name}-{self.branch_code}"
            )
        if not self.store_code:
            self.branch_code=self.generate_branch_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name}-{self.branch_name}"
    

    register = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    opening_cash = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    closing_cash = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    opened_at = models.DateTimeField(
        auto_now_add=True
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_closed = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "register_sessions"

    def __str__(self):
        return f"{self.register.name} Session"