FROM python:3.10

WORKDIR /app

COPY  ../ /app

COPY requirements.txt /app

# RUN source ./django_env/bin/activate
RUN pip install -r ../../requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000