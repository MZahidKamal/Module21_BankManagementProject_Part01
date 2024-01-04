from django.urls import path
from .views import DepositTransaction_View, WithdrawTransaction_View, TransferTransaction_View, LoanRequestTransaction_View, TransactionReport_View, LoanPay_View, LoanHistoryList_View

urlpatterns = [
    path('deposit/', DepositTransaction_View.as_view(), name='deposit'),
    path('withdraw/', WithdrawTransaction_View.as_view(), name='withdraw'),
    path('transfer/', TransferTransaction_View.as_view(), name='transfer'),
    path('loan_request/', LoanRequestTransaction_View.as_view(), name='loan_request'),
    path('transaction_report/', TransactionReport_View.as_view(), name='transaction_report'),
    path('loan_history/', LoanHistoryList_View.as_view(), name='loan_history'),
    path('loan_pay/<int:loan_request_id>/', LoanPay_View.as_view(), name='loan_pay'),
]
