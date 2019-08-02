FROM python:3.7

COPY /requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /
RUN chmod +x /run_api_server.sh

ENTRYPOINT /run_api_server.sh
