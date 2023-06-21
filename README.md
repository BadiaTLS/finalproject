# Run the code
1. Make a virtual environment using python by running python -m venv venv (adjust by your method) inside the directory finalproject.
2. pip install -r requirements.txt
3. cd final_project
4. python manage.py runserver

# MAKE SURE YOUR DATABASE IS ALREADY EMPTY
To check you can go to http://127.0.0.1:8000/admin
and enter
username: admin
password: admin
And delete all the data from the table_classes, table_students, table_times, table_session, and table_user
(The order is up to you, but make sure the table_user is the last)

## Doing Migration after all data in database empty, migration file in each layer deleted,
## and file db.sqlite3 deleted

After all the data in database is deleted, check every layer in the code 

check in this path final_project/final_project/(students, dininghall, accounts)/migrations/

delete every file inside that directory except the __pycache__ and the __init__.py

delete db.sqlite3 in final_project/

### After you make sure doing all the requirements above follow this step
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser
it will show you a some field that need to fill
username: yourchoice
email: yourchoice
password: yourchoice
Bypass password validation and create user anyway? [y/N] y

### After you done doing step above run this code
python manage.py runserver and go to http://127.0.0.1:8000/admin

enter the username and password you create before

Go to Custom users section and click (ADD CUSTOM USER +) in top right below the logout

Fill the user information and make sure you fill every field, click save.

Logout from admin and back to http://127.0.0.1:8000/

Enter the email dan password you create before and enjoy