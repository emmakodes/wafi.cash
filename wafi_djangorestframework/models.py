from django.db import models
from rest_framework import serializers, viewsets

class User(models.Model):
    name = models.CharField(max_length=255)
    balance = models.FloatField(default=0)
