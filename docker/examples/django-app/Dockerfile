FROM python:3.7
ENV PYTHONUNBUFFERED 1
# add custom user and group which should be the one running the service
#RUN groupadd -g 500 customgroup && useradd -r -u 500 -g customgroup customuser
RUN apt-get update -q \
    && apt-get upgrade -qy \
    && apt-get install -y \
        postgresql-client
RUN mkdir /app /static
WORKDIR /app
ADD requirements.txt /app/
ADD django-app/wsgi.py /app/
RUN pip3 install pip --upgrade --force-reinstall \
    && pip3 install -r /app/requirements.txt
ADD . /app/
RUN chown -R 500:500 /app /static
USER customuser
#CMD ["python3", "/app/manage.py", "runserver", "0:8888"]
# keep it on one line, Dockerfile does not support multiline commands
# `uwsgi` must be installed via pip
CMD ["uwsgi", "--http", "0.0.0.0:8888", "--chdir", "/app", "--wsgi-file", "/app/wsgi.py", "--callable", "application", "--processes", "2", "--threads", "4" ]
