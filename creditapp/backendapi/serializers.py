# serializers.py

import random
from rest_framework import serializers
from .models import CustomersInfo,LoanInfo

class CustomerSerializer(serializers.ModelSerializer):
    
    customer_id = serializers.SerializerMethodField()
    approved_limit = serializers.SerializerMethodField()

    class Meta:
        model = CustomersInfo
        fields = ['first_name','last_name', 'age', 'monthly_salary', 'phone_number', 'customer_id', 'approved_limit']

    def get_customer_id(self, obj):
        
        return ''.join(random.choices('0123456789', k=10))

    def get_approved_limit(self, obj):
        
        return round(36 * obj.monthly_salary, -5)

    def create(self, validated_data):
        validated_data['phone_number'] = validated_data['phone_number']
        validated_data['monthly_salary'] = validated_data['monthly_salary']
        validated_data['age'] = validated_data['age']
        validated_data['approved_limit'] = round(36 * validated_data['monthly_salary'], -5)
        validated_data['customer_id'] = ''.join(random.choices('0123456789', k=10))

        return super().create(validated_data)


class CreditScoreCalculatorSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class CustomerSerializeraa(serializers.ModelSerializer):
    class Meta:
        model = CustomersInfo
        fields = ['customer_id', 'first_name','last_name', 'phone_number', 'age']

class LoanInfoSerializer(serializers.ModelSerializer):
    customer_id = CustomerSerializeraa()
    
    class Meta:
        model = LoanInfo
        fields = ['loan_id', 'customer_id', 'loan_amount', 'interest_rate', 'monthly_repayment', 'tenure']

