if exist %~dp0tavenv rmdir /s /q %~dp0tavenv (
    python -m venv tavenv
    echo tavenv created
    echo installing requirements.txt
    timeout /t 5
    call %~dp0tavenv\Scripts\activate.bat
    set PROMPT=(tavenv) $P$G

    if not exist %~dp0final_project\requirements.txt (
        echo final_project\requirements.txt not found
        exit /b
    )
    pip install -r %~dp0final_project\requirements.txt
    call %~dp0tavenv\Scripts\deactivate.bat
) else (
    echo installing requirements.txt
    timeout /t 5
    call %~dp0tavenv\Scripts\activate.bat
    set PROMPT=(tavenv) $P$G

    if not exist %~dp0final_project\requirements.txt (
        echo %~dp0final_project\requirements.txt not found
        exit /b
    )
    pip install -r %~dp0final_project\requirements.txt
    call %~dp0tavenv\Scripts\deactivate.bat
)

echo Getting Ready for migrations
timeout /t 5

call %~dp0tavenv\Scripts\activate.bat
set PROMPT=(tavenv) $P$G

IF EXIST final_project\db.sqlite3 DEL /F final_project\db.sqlite3

python final_project\manage.py makemigrations
python final_project\manage.py migrate

@echo off
set DJANGO_SUPERUSER_USERNAME=admin
set DJANGO_SUPERUSER_EMAIL=admin@example.com
set DJANGO_SUPERUSER_PASSWORD=admin
python final_project\manage.py createsuperuser --noinput

@echo off
echo from final_project.accounts.models import CustomUser; CustomUser.objects.create_user(username='sassas', email='sas@example.com', password='sassas', name='SAS', role='sas') | python final_project\manage.py shell
echo from final_project.accounts.models import CustomUser; CustomUser.objects.create_user(username='dininghall', email='dininghall@example.com', password='dininghall', name='Dining Hall', role='dininghall') | python final_project\manage.py shell

python final_project\manage.py runserver

call tavenv\Scripts\deactivate.bat

pause