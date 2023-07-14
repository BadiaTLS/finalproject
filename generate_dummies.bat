@echo off

echo Please Wait Generating the dummies...

python %~dp0dummy_gen\user_generator.py
timeout /t 1
python %~dp0dummy_gen\menu_gen_v2.py
timeout /t 1
python %~dp0dummy_gen\bookings_gen_v2.py
timeout /t 1
python %~dp0dummy_gen\live_bookings_generator.py
timeout /t 1
python %~dp0dummy_gen\class_generator.py

cls
echo All dummies created
timeout /t 3
