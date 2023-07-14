echo Importing Users...
python %~dp0final_project\manage.py import_users %~dp0data_dummy_users.xlsx

echo DONE
timeout /t 5