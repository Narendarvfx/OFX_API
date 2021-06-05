FROM python:3.6.8 AS ldap-build

RUN apt-get update -y && \
    apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev && \
    python -m pip wheel --wheel-dir=/tmp python-ldap==3.3.1

FROM python:3.6.8
COPY --from=ldap-build /tmp/*.whl /tmp
RUN python -m pip install /tmp/*.whl
FROM python:3.6.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /my-api
WORKDIR /my-api
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./manage.py","makemigrations" ]
CMD [ "python", "./manage.py","migrate" ]
CMD [ "python", "./manage.py","collectstaticfiles" ]
CMD [ "python", "./manage.py","runserver" ]