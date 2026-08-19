from django.db import models
from django.utils import timezone

# Create your models here.

class BaseEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])
    
    def hard_delete(self):
        super().delete()


class TenantQuerySet(models.QuerySet):
    def for_tenant(self, tenant):
        return self.filter(company=tenant)


# class TenantManager(models.Manager):
#     def get_queryset(self):
#         return TenantQuerySet(self.model, using=self._db)

#     def for_request(self, request):
#         return self.get_queryset().for_tenant(request.tenant)

class TenantManager(models.Manager):
    def for_request(self,request):

        user=request.user
        if not user or not user.is_authenticated:
            return self.none()
        company=getattr(user,'tenant',None)
        if not company:
            return self.none()
        return self.filter(company=company)
    
    def get_queryset(self):
        return super().get_queryset()