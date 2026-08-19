from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class CompanyManager(models.Manager):
    """Query-only methods for Company model"""
    
    def get_active_tenants(self):
        """Get all active tenants"""
        return self.filter(is_active=True, is_trial_active=True)
    
    def get_expired_trials(self): 
        """Get tenants with expired trials"""
        return self.filter(is_trial_active=False, is_active=True)
    
    def get_tenant_by_domain(self, domain):
        """Get tenant by domain"""
        from .models import Domain
        try:
            domain_obj = Domain.objects.get(domain=domain)
            return domain_obj.tenant
        except Domain.DoesNotExist:
            return None
    
    def check_trial_status(self):
        """Update trial status for all tenants"""
        now = timezone.now()
        expired = self.filter(trial_end_date__lt=now, is_trial_active=True)
        expired.update(is_trial_active=False)
        return expired.count()