echo Importing Session Menu

python %~dp0final_project\manage.py import_session_menu %~dp0data_dummy_session_menu.csv

echo DONE
timeout /t 5
