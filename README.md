# Profiles REST API

Profiles REST API Code
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
django-admin.py startproject profiles_project .
python manage.py startapp profiles_api
python manage.py runserver

http://127.0.0.1:8000

python manage.py makemigrations profiles_api
python manage.py migrate

python manage.py migrate profiles_api previous_migration



If you want to use Python 3.11 as your default Python version (instead of 3.13), add this line to your ~/.zshrc:

echo "alias python='/opt/homebrew/bin/python3.11'" >> ~/.zshrc
echo "alias pip='/opt/homebrew/bin/python3.11 -m pip'" >> ~/.zshrc
source ~/.zshrc