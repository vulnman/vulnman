# Install Vulnman Server


## Without Docker

### Requirements

#### Fedora
```bash
sudo dnf install python3 nginx git
sudo pip install -r requirements.txt
```

#### Arch-Linux

```
sudo pacman -Sy python nginx git
sudo pip install -r requirements.txt
```

### Prepare
First we fetch the source code.

```bash
mkdir /opt/vulnman-server
git clone https://github.com/vulnman/vulnman.git
cd /opt/vulnman-server
```


### Configure Database
The default settings will use a sqlite database.
If you are fine with this you can continue with this tutorial.
Otherwise, you may want to read how to [configure](../configuration/index.md) your installation.


### Initializing Database
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createupseruser
```

### Systemd Service
If you want to run the vulnman-server using systemd, you can paste the following
content into the `/etc/systemd/system/vulnman-server.service` file.

```
[Unit]
Description=vulnman server
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/opt/vulnman-server
ExecStart=gunicorn --bind 127.0.0.1:8000 vulnman.wsgi

[Install]
WantedBy=multi-user.target
```

To enable the service on boot and start the vulnman service, you can use the following commands:

```bash
sudo systemctl start vulnman-server
sudo systemctl enable vulnman-server
```

### Setup Nginx

Paste the following content into the `/etc/nginx/sites-enabled/vulnman.conf` file

```
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
```


## With docker-compose

Adjust the credentials and paths in the `docker-compose.yml` file.

For the docker image to work, you need to set up vulnman to use a [postgres database](../configuration/index.md#postgresql).



You can start all containers with the following command:

```bash
sudo docker-compose up --build
```

