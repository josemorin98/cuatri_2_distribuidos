FROM python:3.8-buster



#install requeriments
RUN pip install flask
RUN pip install requests
RUN pip install pandas
RUN pip install sklearn

COPY ./ /app
WORKDIR  /app
EXPOSE 5000