FROM python:3.6

RUN adduser wages

WORKDIR /home/wages

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY wages wages
COPY migrations migrations
COPY wages.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP wages.py

RUN chown -R wages:wages ./
USER wages

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]