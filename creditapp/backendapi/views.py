from django.shortcuts import render

# Create your views here.

# views.py

# views.py
import random
from django.http import JsonResponse
from rest_framework import generics
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from .models import CustomersInfo, LoanInfo
from .serializers import CustomerSerializer,CreditScoreCalculatorSerializer,LoanInfoSerializer
from datetime import datetime, date, timedelta
from .models import LoanInfo
from .serializers import CreditScoreCalculatorSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    queryset = CustomersInfo.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Modify the response data before returning
        response_data = self.get_response_data(serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_response_data(self, data):
        # Customize the response data here
        modified_data = {
            'message': 'Customer registered successfully!',
            'customer_id': data.get('customer_id'),
            'name': data.get('first_name')+ ' '+ data.get('last_name'),
            'age':data.get('age'),
            'monthly_income':data.get('monthly_salary'),
            'approved_limit': data.get('approved_limit'),
            'phone_number':data.get('phone_number')
            # Add more fields as needed
        }
        return modified_data

class CreditScoreCalculatorView(generics.CreateAPIView):
    serializer_class = CreditScoreCalculatorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data['customer_id']
        interest_rate=serializer.validated_data['interest_rate']
        tenure=serializer.validated_data['tenure']
        loan_amount=serializer.validated_data['loan_amount']
        loan_amount=int(loan_amount)
        print(customer_id, " hdsfjbdj")

        # Fetch data from LoanInfo model based on customer_id
        try:
            # Assuming 'loans' is the related_name in the LoanInfo model
            loan_info = LoanInfo.objects.filter(customer_id__customer_id=customer_id)
            print(loan_info, " hdvfhb")
        except LoanInfo.DoesNotExist:
            return Response({'error': 'Loan information not found for the specified customer_id'}, status=status.HTTP_404_NOT_FOUND)

        # Calculate credit score using the specified criteria
        credit_score, current_emi_amount, monthly_salary = self.calculate_credit_score(loan_info, serializer.validated_data)
        msg=''
        
        if(credit_score>=50):
            r = (interest_rate / 100) / 12  # Monthly interest rate
            n = tenure  # Tenure in months
            monthly_repayment = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
            # monthly_repayment=0
            return Response({'Customer id':customer_id,'credit_score': credit_score,'Interest rate':interest_rate,'Updated Interest rate':interest_rate,'Tenure':tenure,'montly_repayment':monthly_repayment,'Loan status':'you can take loan at your interest rate','For confirming': f'http://127.0.0.1:8000/create-loan/{customer_id}/{loan_amount}/{interest_rate}/{tenure}/'}, status=status.HTTP_200_OK)
        elif(30<=credit_score<50):
            r = (max(12,interest_rate) / 100) / 12  # Monthly interest rate
            n = tenure  # Tenure in months
            monthly_repayment = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
            # monthly_repayment=0
            return Response({'Customer id':customer_id,'credit_score': credit_score,'Interest rate':interest_rate,'Updated Interest rate':max(12,interest_rate),'Tenure':tenure,'montly_repayment':monthly_repayment,'Loan status':'you can take loan at interest rate greater than 12','For confirming': f'http://127.0.0.1:8000/create-loan/{customer_id}/{loan_amount}/{12}/{tenure}/'}, status=status.HTTP_200_OK)
        elif(10<=credit_score<30):
                r = (max(16,interest_rate) / 100) / 12  # Monthly interest rate
                n = tenure  # Tenure in months
                monthly_repayment = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
                # monthly_repayment=0
                return Response({'Customer id':customer_id,'credit_score': credit_score,'Interest rate':interest_rate,'Updated Interest rate':max(16,interest_rate),'Tenure':tenure,'montly_repayment':monthly_repayment,'Loan status':'you can take loan at interest rate greater than 16','For confirming': f'http://127.0.0.1:8000/create-loan/{customer_id}/{loan_amount}/{16}/{tenure}/'}, status=status.HTTP_200_OK)
        else:
            return Response({'credit_score': credit_score,'Loan_status':'Sorry your loan cant be approved'}, status=status.HTTP_200_OK)
        

    def calculate_credit_score(self, loan_info_objects, input_data):
    # Fetch customer_id from input data
        customer_id = input_data.get('customer_id')

        # Fetch approved_limit from CustomersInfo database based on customer_id
        try:
            customer_info = CustomersInfo.objects.get(customer_id=customer_id)
            # monthly_income=CustomersInfo.objects.get(customer_id=customer_id)
            approved_limit = customer_info.approved_limit
            monthly_income= customer_info.monthly_salary
        except CustomersInfo.DoesNotExist:
            # Handle the case where customer_id is not found
            approved_limit = 0  # Set a default value or handle accordingly

        # Initialize variables for calculation
        past_loans_paid_on_time = 0
        num_loans_taken_in_past = len(loan_info_objects)
        current_year = datetime.now().year
        loan_activity_in_current_year = 0
        current_loans_sum = 0

        for loan_info in loan_info_objects:
            # Calculate past loans paid on time
            start_date = loan_info.start_date
            end_date = loan_info.end_date
            current_emi_amount=0
            months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            print(months_diff)
            if (abs(months_diff - loan_info.emi_on_time) <= 10):
                past_loans_paid_on_time += 1

            # Calculate loan activity in the current year
            if loan_info.end_date.year > current_year:
                loan_activity_in_current_year += 1
                current_emi_amount+=loan_info.monthly_repayment

            # Calculate current loans sum
            if loan_info.end_date.year > current_year:
                current_loans_sum += loan_info.loan_amount

        print(past_loans_paid_on_time, loan_activity_in_current_year, current_loans_sum, num_loans_taken_in_past, " datajkdjksf")
        past_loans_paid_on_time = past_loans_paid_on_time / num_loans_taken_in_past
        if num_loans_taken_in_past > 10:
            num_loans_taken_in_past = 0
        else:
            num_loans_taken_in_past = 1

        if loan_activity_in_current_year > 2:
            loan_activity_in_current_year = 0
        else:
            loan_activity_in_current_year = 1

        if(current_loans_sum> approved_limit):
            return 0
        
        current_loans_sum= 1-(current_loans_sum/approved_limit)
        # Calculate the credit score using the specified weights
        credit_score = ((past_loans_paid_on_time + num_loans_taken_in_past + loan_activity_in_current_year+ current_loans_sum) / 4) * 100

        

        return credit_score, current_emi_amount,monthly_income

class LoanInfoRetrieveView(generics.RetrieveAPIView):
    queryset = LoanInfo.objects.all()
    serializer_class = LoanInfoSerializer
    lookup_field = 'loan_id'

class LoanInfoListView(generics.ListAPIView):
    serializer_class = LoanInfoSerializer

    def get_queryset(self):
        # Get the customer_id from the URL parameters
        customer_id = self.kwargs['customer_id']

        # Retrieve all loans associated with the specified customer_id
        queryset = LoanInfo.objects.filter(customer_id__customer_id=customer_id)
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class CreateLoanInfoView(View):

    def handle_request(self, request, *args, **kwargs):
        if request.method == 'GET' or request.method == 'POST':
            # Extract parameters from the URL
            customer_id = kwargs.get('customer_id')
            loan_amount = kwargs.get('loan_amount')
            interest_rate = float(kwargs.get('interest_rate'))  # Convert interest_rate to float
            tenure = kwargs.get('tenure')

            # Fetch customer information based on customer_id
            try:
                customer_info = CustomersInfo.objects.get(customer_id=customer_id)
            except CustomersInfo.DoesNotExist:
                return JsonResponse({'error': 'Customer information not found for the specified customer_id'}, status=404)

            # Calculate the monthly repayment based on the EMI formula
            r = (interest_rate / 100) / 12  # Monthly interest rate
            n = tenure  # Tenure in months

            emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)

            # Check if the monthly repayment is within the approved limit
            # Create a new LoanInfo object
            loan_id = ''.join(random.choices('0123456789', k=10))
            loan_info = LoanInfo.objects.create(
                customer_id=customer_info,
                loan_id=loan_id,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                tenure=tenure,
                monthly_repayment=emi,
                emi_on_time=tenure,
                start_date=datetime.now().date(),  # Set the start date to the current date
                end_date=datetime.now().date() + timedelta(days=tenure * 30)  # Set the end date based on tenure
            )

            return JsonResponse({'loan_id': loan_id, 'customer_id': customer_id, 'loan_approved': 'Yes', 'monthly_installment': emi}, status=201)

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    def get(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)