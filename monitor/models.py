from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=300)
    def __str__(self):
        return self.url