# wildforge-api

## Running Dev

#### Running DB
```bash
$ cd mysql
$ sudo docker build . -t wildforge-db
$ sudo docker run -d -p 3306:3306 --name wildforge-db -e MYSQL_ROOT_PASSWORD=1234 wildforge-db
```

check if wildforge-db is running 

#### Running Django REST API
```bash
$ python3 backend/manage.py makemigrations && python3 backend/manage.py migrate && python3 backend/manage.py runserver 0.0.0.0:8000
```

### Swagger Endpoint
http://0.0.0.0:8000/swagger/