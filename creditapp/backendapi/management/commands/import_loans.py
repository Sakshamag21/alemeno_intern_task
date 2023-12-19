import pandas as pd
from django.core.management.base import BaseCommand
from backendapi.models import CustomersInfo,LoanInfo

class Command(BaseCommand):
    help = 'Import customers from loan_data.xlsx'

    def handle(self, *args, **options):
        # Clear existing data from CustomersInfo
        self.stdout.write(self.style.SUCCESS('Deleting existing data from LoansInfo...'))
        LoanInfo.objects.all().delete()
        # LoanInfo.objects.all().delete()

        # Import data from customer_data.xlsx
        self.stdout.write(self.style.SUCCESS('Importing data from loan_data.xlsx...'))
        try:
            df = pd.read_excel('loan_data.xlsx')  # Replace with the actual path
            for index, row in df.iterrows():
                try:
                    customer = CustomersInfo.objects.get(customer_id=row['Customer ID'])
                except CustomersInfo.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Customer not found for ID: {row["Customer ID"]}'))
                    continue

                existing_loan = LoanInfo.objects.filter(loan_id=row['Loan ID']).first()
                if existing_loan:
                    self.stdout.write(self.style.WARNING(f'Loan with ID {row["Loan ID"]} already exists. Skipping...'))
                    continue
                LoanInfo.objects.create(
                    customer_id=customer,
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_repayment=row['Monthly payment'],
                    emi_on_time=row['EMIs paid on Time'],
                    start_date=row['Date of Approval'],
                    end_date=row['End Date']
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
