# SHOTBUZZ-WEBAPP
## 1. Prerequisite
<!-- **[Windows x86-64 executable installer](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe "Linux Commands")**  -->
**[Python-3.6.8 Windows x86-64 executable installer](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe "Linux Commands")** 
```shell
python --version
python.exe -m pip install --upgrade pip
python.exe -m pip --version
python.exe -m pip install pipenv
```
<!-- > Install Pyhon plugin in you VS Code editor. -->
## 2.1.1 Create VENV Project
```shell
# pipenv install django==4.0.1
python.exe -m pipenv install django==3.2.12
pip install -r requirements.txt
pip install mysqlclient
pipenv --venv
pipenv shell
# pip install channels==3.0.5
pip install channels==3.0.4
python.exe -m pip install --upgrade pip
# pip install channels
pip show django
pip show channels
```

## 2.1.2 Copy
```python
copy '/websockets/' to '/websockets/'
copy '/api/' to '/api/' #you can provide provide your end point to get wstoken
# copy '/wsdoc/' to '/wsdoc/' #you can provide provide your end point to get wstoken
```
## 2.1.2 Add/Update Lines
> main > asgi.py
```python
# Step 1
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import websockets.routing

# Step 2
# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websockets.routing.websockets_urlpatterns
            )
        )
    # 'websocket': URLRouter(
    #     websockets.routing.websockets_urlpatterns
    #     )
    })
```

> main > settings.py
```python
# Step 1
INSTALLED_APPS = [
    'channels',
    ...
    'api',
    # 'wsdoc'
    ...

# Step 2
# ASGI_APPLICATION = '<your_project_name>.asgi.application'
ASGI_APPLICATION = 'main.asgi.application'

# Step 3
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}
```
> main_app > urls.py (optional)
```python
# Step 1
from django.urls import path, include

# Step 2
urlpatterns = [
    ...
    path('api/',include('api.urls'))
    # path('',include('wsdoc.urls'))
    ...
]
```
## 2.1.3 Apply Migrations
```shell
# pip install airium
# pip install dataclasses
# pip install nltk
pip install mysqlclient-1.4.6-cp36-cp36m-win_amd64.whl
pip install pymysql

python manage.py makemigrations
python manage.py makemigrations profiles
python manage.py makemigrations hrm
python manage.py makemigrations production
python manage.py makemigrations ofx_dashboards
python manage.py makemigrations ofx_statistics
python manage.py makemigrations wsnotifications


python manage.py migrate profiles
python manage.py migrate hrm
python manage.py migrate production
python manage.py migrate ofx_dashboards
python manage.py migrate ofx_statistics
python manage.py migrate wsnotifications

python manage.py migrate
python manage.py migrate --fake-initial
python manage.py makemigrations
python manage.py runserver 7000
python manage.py runserver 192.168.10.8:8000

python3 manage.py dumpdata auth.user > /tmp/fixtures/auth_user.json
python3 manage.py dumpdata hrm.attendance > /tmp/fixtures/hrm_attendance.json
python3 manage.py dumpdata hrm.department > /tmp/fixtures/hrm_department.json
python3 manage.py dumpdata hrm.department > /tmp/fixtures/hrm_department.json

python manage.py loaddata /Users/ofxlap-28/Desktop/auth_user.json --traceback
python manage.py loaddata /Users/ofxlap-28/Desktop/hrm.json --traceback
python manage.py loaddata /Users/ofxlap-28/Desktop/production.json --traceback
python manage.py loaddata /Users/ofxlap-28/Desktop/hrm_per.json --traceback
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/production_clients.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/production_projects.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/production_tasktype.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/production_sequence.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/shots.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/complexity.json
python manage.py loaddata /Users/ofxlap-28/Desktop/prod_fixtures/mytask.json



```