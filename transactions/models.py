from django.db import models
from accounts.models import UserBankAccount_Model

from .constants import TRANSACTION_TYPES

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create your models here.

class Transactions_Model(models.Model):
    account = models.ForeignKey(UserBankAccount_Model, on_delete=models.CASCADE, related_name='transactions')
    receiver_account = models.ForeignKey(UserBankAccount_Model, null=True, blank=True, on_delete=models.SET_NULL, related_name='transfer_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    post_transaction_balance = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TRANSACTION_TYPES, null=True)
    loan_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

