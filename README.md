pegapega
========

Copie o settings_local.py em pegapega/

mkvirtualenv pegapega

workon pegapega

pip install -r requirements.txt

python manage.py syncdb

python manage.py migrate
