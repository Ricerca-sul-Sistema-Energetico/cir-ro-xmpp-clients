# CIR-RO xmpp-client

Source code to istantiate an XMPP client interface compliant to [CEI 0-21 Annex X](https://mycatalogo.ceinorme.it/cei/item/0010019013/?sso=y) and relative [PAS 57-127](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://static.ceinorme.it/strumenti-online/doc/20075.pdf) 

## Description
The software consists in a service instatiation that allows to commuincate with an xmpp server via port 5222. \
The service also allows  to send xmpp messages to a specific client by expliciting a destination jabber id. Sending process is triggered via APIs exposed on port 8000.

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

To start the client service simply run the main.py file from command line 
```bash
python main.py
```
or using any code editor. \
APIs can also be triggered manually via a FastApi interface, which can be accessed from browsers at https://localhost:8000/docs# (substitute localhost with hosting IP if service is not run locally). \ 
Depending on the xmpp client defined in the .env file ("cir" or "ro") different APIs will be available. Wrong configuration makes no API available to appear.

## Usage
There are two ways to use this repository.
### 1- Complete utilization
In this case all the repository is used by downloading all the files, setting up the pyhon environment and running the main.py script. This will istantiate an xmpp communication interface fully compliant with CEI 0-21 and PAS 57-127 perscriptions. Such interface can be directly integrated on a CIR device on in a Remote Operator backend. 
### 2- Partial utilization
If a user decides to autonomously implement its communication interface, it can rely on message json schemas container in the json_schemas folder. Such files allow to create dataobjects compliant to the standards in any programming language, facilitating alternative implementations to this repository. 
Even in this case, a complete istantiation could serve as a communication counterpart to test the self-developed xmpp client.  

## Support
For any support instance, please contact ricarica@rse-web.it

## Remain Updated!
This project is being developed along 2024, and its latest version of the main branch is stable but not ultimate. 
The project progesses are discussed monthly on scheduled meetings between RSE and other project partners. If you are interested in participating please write at ricarica.ev@rse-web.it

