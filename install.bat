python -m venv .venv
pause

cd .venv/Scripts
activate.bat

cd ../..

python -m pip install -U pylint
pause

python -m pip install -U nose
pause

python -m pip install -U pymongo
pause

python -m pip install -U pytz
pause
