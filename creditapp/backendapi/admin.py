from django.contrib import admin

# Register your models here.
from .models import LoanInfo,CustomersInfo

admin.site.register(LoanInfo)
admin.site.register(CustomersInfo)