call %~dp0venv\Scripts\activate.bat

echo %VIRTUAL_ENV%

python final_project\manage.py runserver

call venv\Scripts\deactivate.bat
