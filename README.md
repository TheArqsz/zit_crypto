# Web application that supports cryptoanalysis

Web application made for ZIT course at 5th semester of Cybersecurity at Wrocław University of Science and Technology

## Prerequisites
Scripts are written under **python 3.7.4**

Before you can use it you need to have a few things:
* Linux-based OS (Debian, Ubuntu etc..)
* p7zip-full
* unrar (non-free)
* python 3
	
### Installing required libraries

```
pip install -r requirements.txt
```

### Usage

To run application:

```
gunicorn -c gunicorn.conf.py wsgi
```

App will boot up at default ip and port 127.0.0.1:8080


### Environmental variables

|              ENV              	|       Default Value       	|                          Purpose                         	|
|:-----------------------------:	|:-------------------------:	|:--------------------------------------------------------:	|
|        DATABASE_DIALECT       	|             -             	|                       Dialect of DB                      	|
|         DATABASE_USER         	|             -             	|                        User for DB                       	|
|         DATABASE_PASS         	|             -             	|                      Password for DB                     	|
|          DATABASE_IP          	|             -             	|                         IP of DB                         	|
|         DATABASE_NAME         	|             -             	|                      Name of DB used                     	|
|    ARCHIVE_DECRACK_TIMEOUT    	|             60            	| Time during which archives will be tried to be decrypted 	|
|        MJ_APIKEY_PUBLIC       	|          example          	|               Public key of Mailjet account              	|
|       MJ_APIKEY_PRIVATE       	|          example          	|              Private key of Mailjet account              	|
|          SENDER_EMAIL         	|    example@example.com    	|            Mail from which mails will be sent            	|
|           FLASK_HOST          	|         127.0.0.1         	|              IP under which app will boot up             	|
|           FLASK_PORT          	|            8080           	|           Port under which app will be boot up           	|
|             DEBUG             	|           False           	|                     Is debug mode ON                     	|
