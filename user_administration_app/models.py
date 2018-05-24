from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator')

    def __str__(self):
        user_and_creator = _("{0} - Created by: {1}")
        return user_and_creator.format(self.user, self.creator)

    class Meta:
        ordering = ('user',)


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    iban = models.CharField(max_length=34)  # IBAN max-length is 34, according to Wikipedia.
    owner = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)  # Any user can have more than one bank accounts

    def __str__(self):
        return self.iban

    class Meta:
        ordering = ('iban',)