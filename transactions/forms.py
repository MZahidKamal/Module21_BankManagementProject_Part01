from django import forms
from .models import Transactions_Model

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
