# urls.py

from django.urls import path
from .views import CustomerRegistrationView,CreditScoreCalculatorView,LoanInfoRetrieveView,LoanInfoListView,CreateLoanInfoView

urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register_customer'),
    path('check-eligibility/', CreditScoreCalculatorView.as_view(), name='calculate_credit_score'),
    path('view-loan/<int:loan_id>/', LoanInfoRetrieveView.as_view(), name='loan-info-detail'),
    path('view-loans/<str:customer_id>/', LoanInfoListView.as_view(), name='customer-loans-list'),
    path('create-loan/<str:customer_id>/<int:loan_amount>/<str:interest_rate>/<int:tenure>/', CreateLoanInfoView.as_view(), name='create_loan_info'),

]
