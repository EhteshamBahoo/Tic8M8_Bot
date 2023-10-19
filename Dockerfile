FROM rasa/rasa-sdk:3.6.2

WORKDIR /app

USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install requests

COPY ./actions /app/actions

USER 1001