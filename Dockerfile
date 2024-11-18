FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY campaign_tracker.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP campaign_tracker.py
RUN flask translate compile

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]