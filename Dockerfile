FROM python:3-bullseye

RUN pip install -r requirements.txt && \
    pip install psycopg2-binary && \
    apt update && \
    apt install -y texlive-latex-extra texlive-fonts-extra latexmk && \
    python manage.py create_secret_key

COPY . /app
COPY docker/docker-entrypoint.sh /app
WORKDIR /app

RUN chmod +x /app/docker-entrypoint.sh


ENTRYPOINT ["/app/docker-entrypoint.sh"]
