from django.db import models
import uuid
# Create your models here.
class Customer(models.Model):
    customer_id=models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False,)
    full_name=models.CharField(max_length=255,)
    email=models.EmailField(max_length=225,)
