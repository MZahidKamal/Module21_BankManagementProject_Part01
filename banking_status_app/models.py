from django.db import models

# Create your models here.
class BankingStatus_Model(models.Model):
    banking_service = models.BooleanField(default=True)

    def __str__(self):
        return f"All kind of Banking Facilities and Service are ACTIVE: {self.banking_service}"
