from django.db import models
from django.contrib.auth.models import User, Group

class UserIcon(models.Model):
    name = models.CharField( max_length=30)
    icon = models.URLField(blank=True)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    statement = models.TextField(blank=True)
    icon = models.ForeignKey(UserIcon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user)