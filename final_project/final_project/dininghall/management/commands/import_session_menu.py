import csv
from django.core.management.base import BaseCommand
from final_project.dininghall.models import table_session, table_time
from datetime import time

class Command(BaseCommand):
    help = 'Import menu data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            session_data = []
            time_data = []

            for row in reader:
                session = table_session(
                    date=row['Date'],
                    name=row['Name'],
                    menu=row['Menu']
                )
                session.save()  # Save the session object before creating time objects

                times = create_times(session.name)
                for t in times:
                    time_data.append(table_time(
                        session_id=session,
                        time=t,
                        seat_limit=row['Seat Limit'],
                        available_seat=row['Seat Limit'],
                    ))

            table_time.objects.bulk_create(time_data)

        self.stdout.write(self.style.SUCCESS('Menu data import completed.'))

def create_times(session_name):
    if session_name == "Breakfast":
        times = [
            time(hour=7, minute=0),
            time(hour=7, minute=30),
            time(hour=8, minute=0),
            time(hour=8, minute=30),
        ]
    elif session_name == "Lunch":
        times = [
            time(hour=11, minute=0),
            time(hour=11, minute=30),
            time(hour=12, minute=0),
            time(hour=12, minute=30),
            time(hour=13, minute=0),
            time(hour=13, minute=30),
        ]
    elif session_name == "Dinner":
        times = [
            time(hour=17, minute=0),
            time(hour=17, minute=30),
            time(hour=18, minute=0),
            time(hour=18, minute=30),
            time(hour=19, minute=0),
            time(hour=19, minute=30),
        ]
    else:
        times = []

    return times
