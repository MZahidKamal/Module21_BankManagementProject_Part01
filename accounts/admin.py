from django.contrib import admin
from .models import UserBankAccount_Model, UserAddress_Model

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Register your models here.
admin.site.register(UserBankAccount_Model)
admin.site.register(UserAddress_Model)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
