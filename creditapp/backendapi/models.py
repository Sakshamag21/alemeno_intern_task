
from django.db import models

# Create your models here.
class CustomersInfo(models.Model):
    customer_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100,null=True)
    phone_number = models.BigIntegerField()
    monthly_salary = models.BigIntegerField()
    approved_limit = models.BigIntegerField()
    age = models.IntegerField()
    current_debt = models.IntegerField(default=0)

class LoanInfo(models.Model):
    customer_id = models.ForeignKey(CustomersInfo, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.CharField(max_length=100, primary_key=True)
    loan_amount = models.IntegerField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    monthly_repayment = models.IntegerField()
    emi_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()