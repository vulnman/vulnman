************
Installation
************

Requirements
############

.. note::
    The current default template requires german language support, so you need to install ``latex-babel-german``.


Fedora
******

.. code-block::

    sudo dnf install latexmk texlive-collection-fontsextra texlive-collection-latexextra nginx
    sudo pip install -r requirements.txt
    sudo pip install gunicorn


Arch-Linux
**********

.. code-block::

    sudo pacman -Sy texlive-fontsextra texlive-latexextra nginx
    sudo pip install -r requirements.txt
    sudo pip install gunicorn


Run without Docker
##################

Prepare
*******

.. code-block::

    python manage.py migrate
    python manage.py collectstatic
    python manage.py createupseruser


Create Systemd Service File
***************************

.. code-block::

    sudo nano /etc/systemd/system/vulnman.service

Paste the following content into the file

.. code-block::

    [Unit]
    Description=vulnman server
    After=network.target

    [Service]
    User=user
    Group=user
    WorkingDirectory=/opt/vulnman
    ExecStart=gunicorn --bind 127.0.0.1:8000 vulnman.wsgi

    [Install]
    WantedBy=multi-user.target


Enable the service on boot and start the vulnman service.

.. code-block::

    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn


Setup Nginx
***********

Paste the following content into the `/etc/nginx/sites-enabled/vulnman.conf` file

.. code-block::

    server {
        listen 80;
        return https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        ssl_certificate_key /etc/ssl/your_cert.key;
        ssl_certificate /etc/ssl/your_cert.crt;
        ssl_protocols TLSv1.3;

        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }


Run using Docker Compose
########################

Adjust the credentials and paths in the docker-compose.yml file.

For the docker image to work, you need to add the following content to your local_settings.py file.

.. code-block:: python

    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': 'vulnman',
        'USER': 'vulnman_db_user',
        'PASSWORD': 'dontusethispassword',
      }
    }


you can start all containers with the following command:

.. code-block:: bash

    sudo docker-compose up --build
