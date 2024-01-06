from django.contrib import admin
from .models import Transactions_Model
from .views import send_transaction_confirmation_email

# Register your models here.
# admin.site.register(Transactions_Model)

@admin.register(Transactions_Model)
class TransactionModel_Admin(admin.ModelAdmin):
    list_display = [
        'account',
        'type',
        'amount',
        'loan_approved',
        'post_transaction_balance',
    ]

    def save_model(self, request, obj, form, change):
        previous_balance = obj.account.balance
        requested_loan_amount = obj.amount
        if obj.loan_approved:
            obj.post_transaction_balance = previous_balance + requested_loan_amount
            obj.account.balance = previous_balance + requested_loan_amount
            obj.account.save()
            send_transaction_confirmation_email(obj.account.user, 'Loan Granted Confirmation', obj.amount, obj.account.user.email, 'transactions/loan_granted_email.html')
        super().save_model(request, obj, form, change)
