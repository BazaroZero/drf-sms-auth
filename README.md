# SMS auth on Django Rest

## Usage :envelope:

You should have poetry and docker installed

- Initialize environment and install dependencies

```
poetry install
```

- Create .env file in drf-sms-auth\config directory as in the example

- Run database

```
docker-compose --env-file drf-sms-auth\config\.env up
```

- Apply migrations

```
python manage.py migrate
```

- Run server and check docs at localhost:8000/swagger or redoc

```
python manage.py runserver
```

## Customization :pencil2:

### Sending SMS

Replace dummy function in drf-sms-auth\users\utils.py with your own

### Constants

In settings.py you can edit **CODE_EXPIRATION_SECONDS** and **CODE_RESEND_TIMEOUT**, variables of [simple_jwt](https://github.com/jazzband/djangorestframework-simplejwt) library which is used for tokens implementation etc
