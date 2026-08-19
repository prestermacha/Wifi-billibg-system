from django.db import models
from django_tenants.models import TenantMixin,DomainMixin 
from django.conf import settings
import uuid
from .manager import CompanyManager
from currency.models import Currency
# Create your models here.
LAYOUT_POSITION=(
    ('left','LTR'),
    ('right','RTL')
)

MENU_POSITION=(
    ('top_bottom','Top & Bottom'),
    ('top_header','Top Header'),
    ('bottom_corner','Bottom Corner')
)

DATE_FORMATS = (
    ("DD/MM/YYYY", "DD/MM/YYYY"),
    ("MM/DD/YYYY", "MM/DD/YYYY"),
    ("YYYY-MM-DD", "YYYY-MM-DD"),
)

TIME_FORMATS = (
    ("12h", "12 Hour (AM/PM)"),
    ("24h", "24 Hour"),
)

class Company(TenantMixin,BaseEntity):
    company_id=models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False,)
    company_name= models.CharField(max_length=255,)
    logo=models.ImageField(upload_to='company/',blank=True,null=True)
    schema_name = models.CharField(max_length=63, unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, related_name="company", blank=True,null=True)
    address = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    is_active=models.BooleanField(default=True)


    auto_create_schema=True
    objects=CompanyManager
 
    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.schema_name: 
            # Generate a valid schema_name: prefix to ensure it starts with letter + short uuid hex
            short_uuid = str(self.company_id).replace('-', '')[:12] 
            self.schema_name = f"c{short_uuid}" 
            # Alternative: f"company_{self.company_id.hex[:10]}"
        super().save(*args, **kwargs)
           
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class Domain(DomainMixin):
    pass

class CompanySettings(models.Model):
    company=models.OneToOneField(Company,on_delete=models.CASCADE,related_name='settings',blank=True,null=True)
    layout=models.CharField(max_length=50,choices=LAYOUT_POSITION,default='left')
    menu_position=models.CharField(max_length=50,choices=MENU_POSITION,default='top_bottom')
    timezone = models.CharField(max_length=50, default="Africa/Dar_es_Salaam")
    detect_timezone=models.BooleanField(default=True)
    date_format=models.CharField(max_length=50,choices=DATE_FORMATS, default="DD/MM/YYYY", blank=True,null=True)
    currency=models.ForeignKey(Currency,on_delete=models.PROTECT,null=True,blank=True)
    time_format=models.CharField(max_length=50,choices=TIME_FORMATS,   default="24h", blank=True,null=True)
    receipt_footer = models.TextField(blank=True)
    enable_tax = models.BooleanField(default=True)
    low_stock_alert = models.BooleanField(default=True)
     


class Language(models.Model):
    name=models.CharField(max_length=20,unique=True)
    key=models.CharField(max_length=20,blank=True,null=True)
    flag=models.ImageField(upload_to='company/language/',blank=True,null=True)

    def __str__(self):
        return f"{self.name}"