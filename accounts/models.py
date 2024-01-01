from django.contrib.auth.models import User
from django.db import models
from .constants import ACCOUNT_TYPES, GENDER_TYPES

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create your models here.
class UserBankAccount_Model(models.Model):
    user = models.OneToOneField(User, related_name='user_account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    account_number = models.PositiveIntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES)
    initial_deposited_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} -- {self.account_number}"

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserAddress_Model(models.Model):
    user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} -- {self.street} {self.house}, {self.postal_code} {self.city}, {self.country}"

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
