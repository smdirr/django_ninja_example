from django.db import models
from django.contrib.auth import models as models_auth


class Person(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    birth_date = models.DateField(null=True)
    email = models.EmailField(max_length=254, null=False, unique=True)

    user = models.ForeignKey(to=models_auth.User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
