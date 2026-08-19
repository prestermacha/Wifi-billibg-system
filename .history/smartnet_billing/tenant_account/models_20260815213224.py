from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from .manager import TenantUserManager
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db import connection
phone_regex = RegexValidator(
        regex=r'^(?:\+?\d{1,3}\s?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$',
        message="Phone number must be in a valid format, e.g., +225 123-456-7890, (123) 456-7890, or 1234567890."
    )
USER_TYPE=(
    ('tenant_admin','Client Admin/Owner'),
    ('branch_manager','Branch Manager'),   
    ('market_officer','Market Officer'),
    ('member','Member'),
)
USER_STATUS=(
    ('enabled','Enabled'),
    ('disabled','Disabled'),   
)
STAFF_ID_PREFIX = {
    'tenant_admin': 'STF',
    'branch_manager': 'STF', 
    'market_officer': 'STF',
    'member':'MB'
}
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from .manager import TenantUserManager
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db import connection
phone_regex = RegexValidator(
        regex=r'^(?:\+?\d{1,3}\s?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$',
        message="Phone number must be in a valid format, e.g., +225 123-456-7890, (123) 456-7890, or 1234567890."
    )

USER_TYPE=(
    ('tenant_admin','Client Admin/Owner'),
    ('branch_manager','Branch Manager'),   
    ('market_officer','Market Officer'),
    ('member','Member'),
)
USER_STATUS=(
    ('enabled','Enabled'),
    ('disabled','Disabled'),   
)
STAFF_ID_PREFIX = {
    'tenant_admin': 'STF',
    'branch_manager': 'STF', 
    'market_officer': 'STF',
    'member':'MB'
}


class TenantUser(models.Model):
    staff_id=models.CharField(max_length=20,primary_key=True,unique=True,editable=False,help_text="Auto-generated: e.g., TAD-2025-0001")
    global_user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="tenant_profile",blank=True,null=True, help_text="Linked GlobalUser for Authentication" )
    username=models.CharField(max_length=255,)
    status=models.CharField(max_length=100,choices=USER_STATUS,default="enabled")
    is_active=models.BooleanField(default=True)
    role=models.ForeignKey("roles.Role",on_delete=models.SET_NULL,null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login=models.PositiveIntegerField(default=0)
    registed_date=models.DateTimeField(auto_now_add=True)



    objects=TenantUserManager()
    class Meta:
        db_table='tenant_users'
        indexes=[
            models.Index(fields=["global_user"]),
            models.Index(fields=["staff_id"]),
            # models.Index(fields=["phone_number"]),
            # models.Index(fields=['email']),
            # models.Index(fields=["user_type"]),
        ]


    def __str__(self):
        return f"{self.global_user.email} - {self.staff_id}"
    

    def _generate_staff_id(self):
        """Generate next staff_id like TAD-2025-0001"""

        prefix = "USR"  # fallback

        current_year = timezone.now().strftime("%Y")
        
        # Start atomic transaction to avoid race conditions
        with transaction.atomic():
            # Lock rows for this user_type + year
            last_user = TenantUser.objects.filter(
                staff_id__startswith=f"{prefix}-{current_year}-"
            ).order_by('-staff_id').first()

            if last_user and last_user.staff_id:
                # Extract number: TAD-2025-0005 → 5
                try:
                    last_num = int(last_user.staff_id.split('-')[-1])
                    next_num = last_num + 1
                except (ValueError, IndexError):
                    next_num = 1
            else:
                next_num = 1

            new_staff_id = f"{prefix}-{current_year}-{next_num:04d}"
            
            # Double-check uniqueness (safety)
            while TenantUser.objects.filter(staff_id=new_staff_id).exists():
                next_num += 1
                new_staff_id = f"{prefix}-{current_year}-{next_num:04d}"

            return new_staff_id

    def save(self, *args, **kwargs):
        if not self.staff_id:  # Only generate if not already set
            self.staff_id = self._generate_staff_id()
  
        if not self.global_user:
            self.global_user=self._create_or_get_global_user()
        super().save(*args, **kwargs)

    def get_tenant_id(self):
            return connection.schema_name




    
