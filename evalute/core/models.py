from django.db import models

# Create your models here.

class Ground(models.Model):
    name = models.CharField(max_length=25, null=True)

class Dump(models.Model):
    name = models.CharField(max_length=25, null=True)
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE, null=True)

