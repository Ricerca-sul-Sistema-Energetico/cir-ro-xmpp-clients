# CIR-RO xmpp-client

Source code to instantiate an XMPP client interface compliant to [CEI 0-21 Annex X](https://mycatalogo.ceinorme.it/cei/item/0010019013/?sso=y) and relative [PAS 57-127](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://static.ceinorme.it/strumenti-online/doc/20075.pdf) 

## Description

This software instantiates a python XMPP client that connects to an XMPP server and sends XMPP messages 
compliant with the PAS specifications, which have been translated in the json_schemas. 

In order to use this client and test the XMPP communication, a REST-API is exposed on http://localhost:8000/docs# that
allows accessing the XMPP client communication interface for sending XMPP messages.

All the configurations shall be edited in the .env file (use the 'example.env' file and rename it). 
Depending on the client_type ("cir" or "ro") different APIs will be exposed.


## Getting started
Clone git repository 
```bash
git clone https://github.com/Ricerca-sul-Sistema-Energetico/cir-ro-xmpp-clients.git
```

Make sure you have python 3.11 installed on your machine. Previous python versions have not been tested, but could work as well.  

Install all the required packages reported in requirements.txt 

```bash
pip install -r requirements.txt
```
## Create .env file

The .env file contains all the parameters of your xmpp client. \
.env file must contain all the fields contained in example.env. \
.env file must be compiled with the information provided by repository owners.
Request for xmpp parameters for your company contacting ricarica.ev@rse-web.it 

## Begin testing
The service can be started by simply launching the main.py script or run as Docker container using the Dockerfile. 

### Launch by command line
To start the service simply run the main.py file from command line 
```bash
python main.py
```


### Create containerized service with Docker
The repository also includes a Dockerfile, allowing to istantiate the service inside a Docker conatiner (https://www.docker.com/get-started/).\
After having compiled the .env file, enter the foldet containing the Dockerfile and run the following command inside the command line in order to build the image of your docker service:
```bash
sudo docker build -t docker-image-name .
```
Then, run the docker container. It is important to map docker ports on the hosting machine ports: api inteface exposed on port 8000 and xmpp interface on port 5222.
```bash
sudo docker run -d -p 8000:8000 -p 5222:5222 --restart unless-stopped --name container_name docker-image-name
```

## Usage
There are two ways to use this repository.

### 1- Complete utilization
In this case all the repository is used by downloading all the files, setting up the pyhon environment and running the main.py script. This will istantiate an xmpp communication interface fully compliant with CEI 0-21 and PAS 57-127 perscriptions. Such interface can be directly integrated on a CIR device on in a Remote Operator backend. \
When the service is istantiated, the client does not connect to the server automatically. It remains disconnected until the POST api /connect_to_server is called. In any moment the client connection can be checked using GET /get_connection_status. Manual disconnection using POST /disconnect_from_server.

### 2- Partial utilization
If a user decides to autonomously implement its communication interface, it can rely on message json schemas container in the json_schemas folder. Such files allow to create dataobjects compliant to the standards in any programming language, facilitating alternative implementations to this repository. 
Even in this case, a complete istantiation could serve as a communication counterpart to test the self-developed xmpp client.  

## Support
For any support instance, please contact ricarica@rse-web.it

## Remain Updated!
This project is being developed along 2024, and its latest version of the main branch is stable but not ultimate. 
The project progesses are discussed monthly on scheduled meetings between RSE and other project partners. If you are interested in participating please write at ricarica.ev@rse-web.it

