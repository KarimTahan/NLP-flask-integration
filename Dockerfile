# To install and run this run the run.sh file as sudo
# To install/run manually:
# sudo docker build -t flask-app .
# sudo docker run -p 5000:5000 -d flask-app

FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
