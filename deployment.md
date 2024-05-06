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
python3 -m venv /opt/d4g/venv
source /opt/d4g/venv/bin/activate
python -m pip install poetry==1.4.0
cd /opt/d4g/12_taxobservatory && poetry install
```
