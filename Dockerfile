FROM python:3.8.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV TZ=UTC
WORKDIR  /app
RUN pip install --upgrade pip setuptools
ADD requirements.txt  requirements.txt

RUN python -m venv venv
RUN  ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r /app/requirements.txt && \ 
    pip install gunicorn gevent && \  
    pip cache purge

ADD . .
RUN chmod +x /app/commands/backup_db.sh
RUN chmod +x /app/commands/restore_db.sh
RUN chmod +x /app/commands/clear_sessions.sh
CMD ["/app/commands/backup_db.sh"]

RUN chmod +x /app/bin/django_start.sh
# RUN chmod +x /app/bin/docker_start.sh
# ENTRYPOINT ["/app/bin/docker_start.sh"]
COPY .  /app
RUN chmod +x /app
ENTRYPOINT ["bash","/app/bin/docker_start.sh"]





