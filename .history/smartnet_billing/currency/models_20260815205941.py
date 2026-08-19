from django.db import models
from base.models import BaseEntity

CURRENCY_POSITION=(
    ('front','Front'),
    ('behind','Behind')
)

# Create your models here.
class Currency(BaseEntity):
    name=models.CharField(max_length=20,unique=True)
    symbol=models.CharField(max_length=20,)
    position=models.CharField(max_length=20,choices=CURRENCY_POSITION,default='behind')
    currency_code=models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return f"{self.name}-{self.symbol}"