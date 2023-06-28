call %~dp0tavenv\Scripts\activate.bat
set PROMPT=(tavenv) $P$G

echo %VIRTUAL_ENV%
echo %PROMPT%

python final_project\manage.py runserver

call tavenv\Scripts\deactivate.bat
pause