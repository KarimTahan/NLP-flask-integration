# To install and run this run the run.sh file as sudo
# To install/run manually:
# sudo docker build -t flask-app .
# sudo docker run -p 5000:5000 -d flask-app

RUN pip install Flask
RUN pip install flask_cors
RUN pip install tensorflow

WORKDIR /app

COPY templates ./templates
COPY char_mappings char_mappings
COPY checkpoints checkpoints
COPY generator.py .
COPY app.py .

COPY . .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
