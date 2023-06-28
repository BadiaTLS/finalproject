if exist %~dp0tavenv rmdir /s /q %~dp0tavenv (
    python -m venv tavenv
    timeout /t 5
    call %~dp0tavenv\Scripts\activate.bat
    set PROMPT=(tavenv) $P$G

    if not exist requirements.txt (
        echo requirements.txt not found
        exit /b
    )
    pip install -r requirements.txt
    call %~dp0tavenv\Scripts\deactivate.bat
)

echo tavenv exist
pause