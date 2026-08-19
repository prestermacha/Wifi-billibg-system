from django.core.management.base import BaseCommand
from currency.models import Currency

class Command(BaseCommand):
    help = "Seed default currencies"

    def handle(self, *args, **kwargs):

        currencies = [
            ("TZS", "Tanzanian Shilling", "TSh"),
            ("USD", "US Dollar", "$"),
            ("KES", "Kenyan Shilling", "KSh"),
            ("UGX", "Ugandan Shilling", "USh"),
            ("EUR", "Euro", "€"),
        ]

        for code, name, symbol in currencies:
            Currency.objects.get_or_create(
                currency_code=code,
                defaults={
                    "name": name,
                    "symbol": symbol,
                }
            )

        self.stdout.write(
            self.style.SUCCESS("Currencies seeded successfully")
        )