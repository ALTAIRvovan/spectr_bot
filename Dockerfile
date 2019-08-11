FROM python:3-alpine
WORKDIR /spectrum
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
VOLUME /spectrum/conf
WORKDIR /spectrum/src
#ENTRYPOINT ["python", "celery", "-A", "run_celery", "worker", "-B"]