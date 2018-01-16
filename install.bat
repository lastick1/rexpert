python -m venv .venv

cd .venv/Scripts
call activate.bat

cd ../..

python -m pip install -U pylint

python -m pip install -U nose

python -m pip install -U pymongo

python -m pip install -U pytz
pause
