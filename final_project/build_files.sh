pip install -r requirements.txt

# make migrations
python3.9 final_project\manage.py makemigrations
python3.9 final_project\manage.py migrate

# create superuser
set DJANGO_SUPERUSER_USERNAME=admin
set DJANGO_SUPERUSER_EMAIL=admin@example.com
set DJANGO_SUPERUSER_PASSWORD=admin
python manage.py createsuperuser --noinput

python3.9 manage.py collectstatic