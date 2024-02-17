FROM tiangolo/uvicorn-gunicorn:python3.11

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app

# Make the script executable
RUN chmod +x /app/start-reload.sh

# Use the script as the entry point or command
CMD ["/app/start-reload.sh"]