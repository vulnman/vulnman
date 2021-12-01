FROM python:3-bullseye

COPY . /app
COPY docker/docker-entrypoint.sh /app
WORKDIR /app

RUN chmod +x /app/docker-entrypoint.sh

RUN pip install -r requirements.txt && pip install psycopg2-binary && python manage.py create_secret_key

VOLUME ["/app/vulnman/secret_key.py"]

ENTRYPOINT ["/app/docker-entrypoint.sh"]
