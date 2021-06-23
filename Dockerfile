FROM python:3.9

ADD . /webapp

ENV HOME /webapp
WORKDIR /webapp

RUN apt update && \
    echo "Installing python3-dev" && \
    apt install -y python3-dev && \
    echo "Installing pipenv" && \
    pip3 install pipenv && \
    echo "Generating requirements.txt" && \
    pipenv lock -r > requirements.txt && \
    echo $(cat requirements.txt) && \
    echo "Uninstalling pipenv" && \
    pip3 uninstall --yes pipenv && \
    echo "Installing requirements.txt" && \
    pip3 install --no-cache-dir -r requirements.txt && \
    echo "Removing python3-dev" && \
    apt remove -y python3-dev

ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:8080", "--wsgi-file", "wsgi.py", "--callable", "app", "--processes", "1", "--threads", "8"]