FROM python:3.6

# Update Ubuntu Software repository
RUN apt-get update; apt-get clean
RUN apt-get -y install sudo
RUN apt-get install python3-pip
RUN pip3 install requests
RUN pip3 install subprocess
RUN pip3 install cgi
RUN pip3 install io
RUN pip3 install os
RUN pip3 install json


COPY webhttpclient.py /webhttpclient.py

CMD ["python3", "webhttpclient.py"]
