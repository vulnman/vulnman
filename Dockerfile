FROM python:3-slim

COPY . /app
WORKDIR /app

RUN apt update && apt install -y fonts-font-awesome libldap2-dev libsasl2-dev gcc libffi-dev\
    libcairo-gobject2 libpango-1.0-0 libpangoft2-1.0-0 git

RUN pip install -r requirements.txt && \
    pip install django-auth-ldap && \
    pip install psycopg2-binary


COPY docker/docker-entrypoint.sh /app
RUN chmod +x /app/docker-entrypoint.sh


ENTRYPOINT ["/app/docker-entrypoint.sh"]
