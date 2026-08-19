from django.dispatch import receiver
from django.db.models.signals import post_save
from companies.models import Company,CompanySettings
from currency.models import Currency
# from company.management.commands.seed_currency  import seed_default_currencies
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import GlobalUser
from branches.models import Branch


@receiver(post_save, sender=Company)
def handle_company_settings(sender,instance,created,**kwargs):
    try:
        if created:
            currency=Currency.objects.get(currency_code='TZS')
            CompanySettings.objects.create(
                company=instance,
                currency=currency,
                timezone="Africa/Dar_es_Salaam",
            )
    
    except Exception as e:
        print(f'Failed during company onboarding {e}')




@receiver(post_save,sender=GlobalUser)
def assign_permissons_to_tenant_admin(sender,instance,created,**kwargs):

    if not created:
        return
    
    if instance.is_verified and instance.is_staff  and not instance.is_superuser:
        content_type=ContentType.objects.get_for_model(Branch)
        permission=Permission.objects.filter(content_type=content_type)
        instance.user_permissions.set(permission)
        instance.save()
        