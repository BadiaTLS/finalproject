from django.core.management.base import BaseCommand
import pandas as pd
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from final_project.accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Import users from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        data = pd.read_excel(excel_file)

        for _, row in data.iterrows():
            try:
                hashed_password = make_password(row['username'], hasher='pbkdf2_sha256')
                user = CustomUser.objects.create(
                    username=row['username'],
                    email=row['email'],
                    name=row['name'],
                    role=row['role'],
                    password = hashed_password,
                    gender=row['gender'],
                    major=row['major']
                )
                # self.stdout.write(self.style.SUCCESS(f"User '{user.email}' imported successfully."))
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(f"Skipping user with email '{row['email']}' due to UNIQUE constraint violation."))

        self.stdout.write(self.style.SUCCESS('User import completed.'))
