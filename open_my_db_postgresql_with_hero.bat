@echo off
REM set PostgreSQL password
set PGPASSWORD=my_db@123

REM connect to my_db database as hero user
psql -U hero -d my_db
