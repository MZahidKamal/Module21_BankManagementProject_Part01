from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Transactions_Model
from accounts.models import UserBankAccount_Model
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransactionsModel_Form(forms.ModelForm):
    class Meta:
        model = Transactions_Model
        fields = [
            'amount',           # Amount will be given by the account holder
            'type',             # Type will be selected by the backend system
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['type'].disabled = True                 # Transaction type input field will be disabled.
        self.fields['type'].widget = forms.HiddenInput()    # And the input field of the form will be hidden.

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.post_transaction_balance = self.account.balance       # Account balance will be updated.
        return super().save()


class TransferTransactionModel_Form(TransactionsModel_Form):
    class Meta(TransactionsModel_Form.Meta):
        fields = TransactionsModel_Form.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class DepositTransaction_Form(TransactionsModel_Form):
    def clean_amount(self):                                 # Here 'clean_' is built in, used with 'amount', to get the clean amount.
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')            # amount is getting from the form filled by the user, and saved into 'amount' variable.
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'Minimum deposit amount is {min_deposit_amount}€.')
        return amount

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class WithdrawTransaction_Form(TransactionsModel_Form):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 5
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')            # amount is getting from the form filled by the user, and saved into 'amount' variable.

        if amount > balance:
            raise forms.ValidationError(f"Insufficient balance.")

        if amount < min_withdraw_amount:
            raise forms.ValidationError(f"Minimum withdrawal amount is {min_withdraw_amount}€.")

        if amount > max_withdraw_amount:
            raise forms.ValidationError(f"Maximum withdrawal amount is {max_withdraw_amount}€.")

        return amount

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransferTransaction_Form(TransferTransactionModel_Form):
    account_number = forms.IntegerField(required=True, label='Receiver Account Number')
    # The field for the receiver account number.

    class Meta:
        model = Transactions_Model
        fields = TransactionsModel_Form.Meta.fields + ['account_number', 'amount']

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        try:
            receiver_account = UserBankAccount_Model.objects.get(account_number=account_number)
        except UserBankAccount_Model.DoesNotExist:
            raise forms.ValidationError(f"Account number {account_number} does not exist.")
        self.cleaned_data['receiver_account'] = receiver_account
        return account_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')                                # amount is getting from the form filled by the user.

        sender_account = self.account
        min_transfer_amount = 1
        max_transfer_amount = 20000
        sender_balance = sender_account.balance

        if amount > sender_balance:
            raise ValidationError("Insufficient balance.")
        if amount < min_transfer_amount:
            raise ValidationError(f"Minimum transfer amount is {min_transfer_amount}€.")
        if amount > max_transfer_amount:
            raise ValidationError(f"Maximum transfer amount is {max_transfer_amount}€.")
        return amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'receiver_account' in self.fields:
            del self.fields['receiver_account']

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoanRequestTransaction_Form(TransactionsModel_Form):
    def clean_amount(self):
        account = self.account
        current_balance = account.balance
        min_loan_amount = 1000
        max_loan_amount = 100000
        amount = self.cleaned_data.get('amount')            # amount is getting from the form filled by the user, and saved into 'amount' variable.
        if current_balance <= 0:
            raise forms.ValidationError(f"Account {account.account_number} is not eligible for loan request.")
        if amount < min_loan_amount:
            raise forms.ValidationError(f"Minimum loan amount is {min_loan_amount}€.")
        if amount > max_loan_amount:
            raise forms.ValidationError(f"Maximum loan amount is {max_loan_amount}€.")
        return amount

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
