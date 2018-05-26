from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator')

    def __str__(self):
        return "{0} {1}".format(self.firstname, self.lastname)

    class Meta:
        ordering = ('firstname',)


class BankAccount(models.Model):
    iban = models.CharField(max_length=34)  # IBAN max-length is 34, according to Wikipedia.
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL)  # We assume any user can have several bank accounts

    def __str__(self):
        return self.iban

    class Meta:
        ordering = ('owner',)
