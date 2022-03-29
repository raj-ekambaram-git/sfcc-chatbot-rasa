FROM rasa/rasa-sdk:2.8.4

WORKDIR /app

COPY actions /app/actions

COPY actions/requirements-actions.txt .

COPY constants /app/constants

COPY client /app/client

COPY utils /app/utils

COPY custom_exception.py .

USER root

RUN pip install --no-cache-dir -r requirements-actions.txt

RUN python client/setup.py install

USER 1001

EXPOSE 5055
