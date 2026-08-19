from permissions.seeders import seed_permissions
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed system permissions"

    def handle(self, *args, **kwargs):

        seed_permissions()

        self.stdout.write(
            self.style.SUCCESS(
                "Permissions seeded successfully"
            )
        )