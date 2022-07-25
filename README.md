# shering-api

## Usage

You should have poetry and docker installed

 - Initialize environment and install dependencies 
 
```
poetry install
```

- Create .env file in shering\config directory as in the example 

- Run database

```
docker-compose --env-file shering\config\.env up
```

- Apply migrations

```
python manage.py migrate
```

- Run server and check docs at localhost:8000/swagger or redoc 

```
python manage.py runserver
```
