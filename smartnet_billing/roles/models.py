from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
from companies.models import Company
from base.models import BaseEntity
from permissions.models import  CustomPermission


class Role(BaseEntity):
    """
    Tenant-level role model for SaaS POS.
    Each company can define its own roles.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="roles"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    permissions = models.ManyToManyField(
        CustomPermission,
        blank=True,
        related_name="roles"
    )
    is_system = models.BooleanField(
        default=False,
        help_text="System roles cannot be deleted by tenant admin"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_roles"
    )

    # created_at = models.DateTimeField(auto_now_add=True)

    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["-created_at"]

    def __str__(self):
        # return f"{self.company.company_name} - {self.name}"
        return f"{self.name}"

    def has_permission(self, codename: str) -> bool:
        """
        Helper method to check permission quickly.
        """
        return self.permissions.filter(codename=codename).exists()





# # class CompanyManager(models.Manager):

#     @transaction.atomic
#     def create_company_with_owner(
#         self,
#         company_name,
#         owner_email,
#         password
#     ):

#         # 1. create company
#         company = self.create(
#             company_name=company_name
#         )

#         # 2. create global user
#         global_user = GlobalUser.objects.create_user(
#             email=owner_email,
#             password=password,
#             phone_number="255700000000",
#             user_type="tenant_user"
#         )

#         # 3. create roles
#         admin_role = Role.objects.create(
#             company=company,
#             name="Admin",
#             slug="admin",
#             is_system=True
#         )

#         # 4. assign all permissions
#         admin_role.permissions.set(
#             CustomPermission.objects.all()
#         )

#         # 5. create tenant profile
#         tenant_user = TenantUser.objects.create(
#             global_user=global_user,
#             company=company,
#             role=admin_role,
#             username="Owner"
#         )

#         return company