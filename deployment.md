# How to deploy the applications

## Initial setup

We start by creating a dedicated user and a specific group

```
sudo groupadd d4gtaxobs
sudo useradd d4gtaxobs --create-home --shell /bin/bash
```

Note: we can add other users to the `d4gtaxobs` group, these will have the
permissions to manipulate the cloned repository and service files with `usermod -a -G d4gtaxobs THE_USER_TO_ADD`

We also install additional system packages 

```
sudo apt install -y git python3-venv
```

## Clone the repository

Now we clone the repository with the `https` URL 

```
sudo mkdir /opt/d4g
sudo chown d4gtaxobs:d4gtaxobs /opt/d4g
sudo su d4gtaxobs
git clone https://github.com/dataforgoodfr/12_taxobservatory.git /opt/d4g/12_taxobservatory
```

## Create the initial virtualenvironment

As `d4gtaxobs` user :

```
sudo su d4gtaxobs
python3 -m venv /opt/d4g/venv
source /opt/d4g/venv/bin/activate
python -m pip install poetry==1.4.0
cd /opt/d4g/12_taxobservatory && poetry install
```

## Test the running code

If you want to test the code is correctly running, you can :

```
sudo su d4gtaxobs
source /opt/d4g/venv/bin/activate
cd /opt/d4g/12_taxobservatory/dataviz
streamlit run data4good.py --server.port 8090
```

And then connect your browser to `http://localhost:8090`.

If the access to the remote server is limited, you may need to use a ssh tunnel :

```
ssh -L 8090:localhost:8090  YOUR_LOGIN@THE_IP_OF_THE_MACHINE
```

## Seting up the apache2 servers, firewall with https certificates

### Firewall

By default, we can access the port `80`, but we will bind our two webservers to
different ports and we need to open the firewall on these ports.

```
sudo apt install ufw
sudo ufw enable
sudo ufw allow 8080/tcp
sudo ufw allow 8090/tcp
```

You can check the opened ports :

```
sudo lsof -i -n -P | grep LISTEN
```

You should have at least the ports `22` for sshd, `8080` and `8090` for our 2
servers. Note, I'm not sure but you may need to wait for apache2 setup as below
(especially the Listen directives) to see them in the lsof list.

### Basic apache2 setup

We expect you have a running apache2 server. If you have a default apache2
installation, you can check for example that :

```
ssh -L 8080:localhost:80  YOUR_LOGIN@THE_IP_OF_THE_MACHINE
```

and then opening a browser on [http://localhost:8080](http://localhost:8080) is
working and opening the default apache2 page.

We then need to ensure some apache2 modules are activated :

```
sudo a2enmod rewrite proxy proxy_http
```

We also need to ask apache2 to listen to more than one port. You need to edit
`/etc/apache2/ports.conf` and replace `Listen 80` by :

```
Listen 8080
Listen 8090
```

We can then define our two apache2 sites that will proxy to the streamlit apps.
Place the following two files in `/etc/apache2/sites-available/`

***/etc/apache2/sites-available/001-taxobs-dataviz.conf***
```
<VirtualHost *:8080>
   RewriteEngine On
   RewriteCond %{HTTP:Upgrade} =websocket
   RewriteRule /(.*) ws://localhost:8081/$1 [P]
   RewriteCond %{HTTP:Upgrade} !=websocket
   RewriteRule /(.*) http://localhost:8081/$1 [P]
   ProxyPassReverse / http://localhost:8081
</VirtualHost>
```

***/etc/apache2/sites-available/002-taxobs-extract.conf***
```
<VirtualHost *:8090>
   RewriteEngine On
   RewriteCond %{HTTP:Upgrade} =websocket
   RewriteRule /(.*) ws://localhost:8091/$1 [P]
   RewriteCond %{HTTP:Upgrade} !=websocket
   RewriteRule /(.*) http://localhost:8091/$1 [P]
   ProxyPassReverse / http://localhost:8091
</VirtualHost>
```

And then let us activate these sites :

```
sudo a2ensite 001-taxobs-dataviz.conf
sudo a2ensite 002-taxobs-extract.conf
```


### Https certificates


## Installing a cron task for automatic update of the repository

TBD

## Setting up service files 

In order to easily start/stop the webservers and to ensure they are started on
machine boot, we can define service files.

### Service file for dataviz

We create the following two files :

***/opt/d4g/service-dataviz.sh***
```{.bash}
#!/bin/bash
      
source /opt/d4g/venv/bin/activate
cd /opt/d4g/12_taxobservatory/dataviz                                               
nohup streamlit run data4good.py --server.port 8081
```

***/etc/systemd/system/d4g-taxobs-dataviz.service***
```{.bash}
[Unit]
Description=D4G TaxObservatory dataviz website
User=d4gtaxobs

[Service]
Type=simple
ExecStart=/opt/d4g/service-dataviz.sh

[Install]
WantedBy=multi-user.target
```

and set the permissions `sudo chmod 644 /etc/systemd/system/d4g-taxobs-dataviz.service`. You should be able to start the service with `sudo service start d4g-taxobs-dataviz`. We can then enable it on startup :

```
sudo service enable d4g-taxobs-dataviz
```

### Service file for extraction

We create the following two files :

***/opt/d4g/service-extract.sh***
```{.bash}
#!/bin/bash
      
source /opt/d4g/venv/bin/activate
cd /opt/d4g/12_taxobservatory 
nohup streamlit run app/index.py --server.port 8091
```

***/etc/systemd/system/d4g-taxobs-extract.service***
```{.bash}
[Unit]
Description=D4G TaxObservatory extract website
User=d4gtaxobs

[Service]
Type=simple
ExecStart=/opt/d4g/service-extract.sh

[Install]
WantedBy=multi-user.target
```

and set the permissions `sudo chmod 644 /etc/systemd/system/d4g-taxobs-extract.service`. You should be able to start the service with `sudo service start d4g-taxobs-extract`. We can then enable it on startup :

```
sudo service enable d4g-taxobs-extract
```
