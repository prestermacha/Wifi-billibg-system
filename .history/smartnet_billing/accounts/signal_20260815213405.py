from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Company,CompanySettings
from currency.models import Currency
# from company.management.commands.seed_currency  import seed_default_currencies
 


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


