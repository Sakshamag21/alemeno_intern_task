import pandas as pd
from django.core.management.base import BaseCommand
from backendapi.models import CustomersInfo,LoanInfo

class Command(BaseCommand):
    help = 'Import customers from customer_data.xlsx'

    def handle(self, *args, **options):
        # Clear existing data from CustomersInfo
        self.stdout.write(self.style.SUCCESS('Deleting existing data from CustomersInfo...'))
        CustomersInfo.objects.all().delete()
        # LoanInfo.objects.all().delete()

        # Import data from customer_data.xlsx
        self.stdout.write(self.style.SUCCESS('Importing data from customer_data.xlsx...'))
        try:
            df = pd.read_excel('customer_data.xlsx')  # Replace with the actual path
            for index, row in df.iterrows():
                CustomersInfo.objects.create(
                    customer_id=row['Customer ID'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    age=row['Age'],
                    phone_number=row['Phone Number'],
                    monthly_salary=row['Monthly Salary'],
                    approved_limit=row['Approved Limit']
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
