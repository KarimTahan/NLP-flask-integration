FROM python:3.7-stretch

RUN pip install Flask
RUN pip install tensorflow

ENV FLASK_APP=app.py

COPY templates ./templates
COPY shakespeare_map.csv .
COPY shakespeare_checkpoint ./shakespeare_checkpoint
COPY generator.py .
COPY app.py .

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0"]