python -m venv .venv

cd .venv/Scripts
call activate.bat

cd ../..

python -m pip install -U pylint

python -m pip install -U nose

python -m pip install -U pymongo

python -m pip install -U pytz

python -m pip install -U rope

python -m pip install -U pillow

python -m pip install -U imageio

python -m pip install -U rx
pause
