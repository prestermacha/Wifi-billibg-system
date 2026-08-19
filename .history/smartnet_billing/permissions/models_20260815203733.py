from django.db import models

# Create your models here.
class CustomPermission(models.Model):
    """Fine-grained permissions per feature."""
    
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    module = models.CharField(max_length=50) 

    def __str__(self):
        return self.codename  