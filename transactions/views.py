from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Transactions_Model
from .forms import DepositTransaction_Form, WithdrawTransaction_Form, TransferTransaction_Form, LoanRequestTransaction_Form
from .constants import DEPOSIT, WITHDRAW, TRANSFER, LOAN_REQUEST, LOAN_PAID
from accounts.models import UserBankAccount_Model
from banking_status_app.models import BankingStatus_Model

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create your views here.

def send_transaction_confirmation_email(user, subject, amount, target_email, template_name='transactions/confirmation_email.html'):
    email_subject = subject
    message = render_to_string(template_name, {
        'user': user,
        'amount': amount,
    })
    to_email = target_email
    send_email = EmailMultiAlternatives(email_subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransactionCreationMixin_View(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transactions_Model
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.user_account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['head_title'] = self.page_title
        context.update({
            'title': self.title
        })
        return context

"""We will be using this view, through inheritance, to create all other views, which is related to transaction."""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransferCreationMixin_View(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transfer_form.html'
    model = Transactions_Model
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.user_account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context

"""We will be using this view, through inheritance, to create all other views, which is related to transaction."""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class DepositTransaction_View(TransactionCreationMixin_View):
    form_class = DepositTransaction_Form
    title = 'Deposit Money'

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = DEPOSIT
        return initial

    def form_valid(self, form):
        user = self.request.user
        amount = form.cleaned_data['amount']
        account = self.request.user.user_account

        # Checking the banking status, if the services are active or declared bankrupt.
        status_check = BankingStatus_Model.objects.first()
        if not status_check.banking_service:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            return self.form_invalid(form)

        account.balance += amount
        account.save(update_fields=['balance'])
        messages.success(self.request, f'{amount}€ was successfully deposited!')
        send_transaction_confirmation_email(user, 'Deposit Transaction Confirmation', amount, 'transactions/deposit_email.html')

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class WithdrawTransaction_View(TransactionCreationMixin_View):
    form_class = WithdrawTransaction_Form
    title = 'Withdraw Money'

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = WITHDRAW
        return initial

    def form_valid(self, form):
        user = self.request.user
        amount = form.cleaned_data['amount']
        account = self.request.user.user_account

        # Checking the banking status, if the services are active or declared bankrupt.
        status_check = BankingStatus_Model.objects.first()
        if not status_check.banking_service:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            return self.form_invalid(form)

        account.balance -= amount
        account.save(update_fields=['balance'])
        messages.success(self.request, f'{amount}€ was successfully withdrawn!')
        send_transaction_confirmation_email(user, 'Withdraw Transaction Confirmation', amount, 'transactions/withdraw_email.html')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransferTransaction_View(TransferCreationMixin_View):
    form_class = TransferTransaction_Form
    title = 'Transfer Money'

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = TRANSFER
        return initial

    def form_valid(self, form):
        user = self.request.user
        user_account = self.request.user.user_account

        # Checking the banking status, if the services are active or declared bankrupt.
        status_check = BankingStatus_Model.objects.first()
        if not status_check.banking_service:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            return self.form_invalid(form)

        # Get the receiver_account directly from cleaned_data
        receiver_account = form.cleaned_data.get('receiver_account')
        amount = form.cleaned_data['amount']

        user_account.balance -= amount
        user_account.save(update_fields=['balance'])

        receiver_account.balance += amount
        receiver_account.save(update_fields=['balance'])

        messages.success(self.request, f'{amount}€ was successfully transferred to the account number {receiver_account.account_number}!')

        send_transaction_confirmation_email(user, 'Transfer Transaction Confirmation', amount, user.email, 'transactions/transfer_sender_email.html')
        send_transaction_confirmation_email(receiver_account, 'Transfer Transaction Confirmation', amount, receiver_account.user.email, 'transactions/transfer_receiver_email.html')

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoanRequestTransaction_View(TransactionCreationMixin_View):
    form_class = LoanRequestTransaction_Form
    title = 'Request For Loan'

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = LOAN_REQUEST
        return initial

    def form_valid(self, form):
        user = self.request.user
        amount = form.cleaned_data['amount']
        account = self.request.user.user_account

        # Checking the banking status, if the services are active or declared bankrupt.
        status_check = BankingStatus_Model.objects.first()
        if not status_check.banking_service:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            return self.form_invalid(form)

        # Loan eligibility check.
        current_loan_count = Transactions_Model.objects.filter(account=account, type=LOAN_REQUEST, loan_approved=True).count()
        if current_loan_count >= 3:
            return HttpResponse('You have reached the maximum number of loan requests!')

        messages.success(self.request, f'Loan request for {amount}€ was successfully submitted!')
        send_transaction_confirmation_email(user, 'Loan Request Confirmation', amount, 'transactions/loan_request_email.html')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TransactionReport_View(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transactions_Model
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.user_account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            )

            self.balance = Transactions_Model.objects.filter(
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']

        else:
            self.balance = self.request.user.user_account.balance

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.user_account
        })
        return context

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoanPay_View(LoginRequiredMixin, View):
    def get(self, request, loan_request_id):
        loan_request = get_object_or_404(Transactions_Model, id=loan_request_id)

        if loan_request.loan_approved:
            user_account = loan_request.account

            if loan_request.amount < user_account.balance:
                user_account.balance -= loan_request.amount

                loan_request.post_transaction_balance = user_account.balance
                # user_account.save(update_fields=['balance'])
                user_account.save()
                loan_request.loan_approved = True
                loan_request.type = LOAN_PAID
                # loan_request.save(update_fields=['type'])
                loan_request.save()
                messages.success(self.request, f'Loan of {loan_request.amount}€ has been approved!')
                return redirect('loan_history')
            else:
                messages.error(self.request, 'Insufficient balance to pay the loan!')
                return redirect('loan_history')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoanHistoryList_View(LoginRequiredMixin, ListView):
    template_name = 'transactions/loan_request.html'
    model = Transactions_Model
    context_object_name = 'loan_request'

    def get_queryset(self):
        user_account = self.request.user.user_account
        queryset = super().get_queryset().filter(
            account=user_account,
            type=LOAN_REQUEST,
            # loan_approved=True
        )
        return queryset

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
