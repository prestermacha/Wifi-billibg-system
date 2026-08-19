from .models import CustomPermission
from .constant import PERMISSIONS
def seed_permissions():
    for codename,name,module in PERMISSIONS:
        CustomPermission.objects.get_or_create(
            codename=codename,
            defaults={
                "name":name,
                "module":module
            }
        )
        print("Permissions seeded successfully") 