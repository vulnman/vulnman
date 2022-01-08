FROM python:3-bullseye

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt && \
    pip install psycopg2-binary
    # && \
    #python manage.py create_secret_key


COPY docker/docker-entrypoint.sh /app
RUN chmod +x /app/docker-entrypoint.sh


ENTRYPOINT ["/app/docker-entrypoint.sh"]
