FROM 	python:3.8
USER 	root

RUN 	echo 'deb http://http.us.debian.org/debian stable main contrib non-free' > /etc/apt/sources.list.d/wheezy.non-free.list
RUN		apt-get update -y && apt-get install -y bash nano git p7zip-full unrar
RUN 	mkdir -p /app 

WORKDIR	/app

COPY 	. /app/zit_crypto/

RUN 	cd zit_crypto && pip3 install -r requirements.txt 
RUN 	groupadd -r gunicorn && useradd --no-log-init -r -g gunicorn gunicorn && chown -R gunicorn /app && chgrp -R gunicorn /app

USER	gunicorn

WORKDIR /app/zit_crypto

ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "wsgi"]
