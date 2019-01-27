FROM centos:latest

#MAINTANER Your Name "ankit864p@gmail.com"

RUN yum install -y  epel-release && yum install -y  python-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./source_code /app

ENTRYPOINT [ "python" ]

CMD [ "web.py" ]
