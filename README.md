## 🛠 Service Booking API

## Create virtual environment

```bash
python -m venv venv
```

### Install all requirements

```bash
pip install -r requirements/base.txt
```

### Then, Change database connection credentials. After that, migrate database

```bash
python manage.py migrate
```

### Create Superuser


```bash
python manage.py createsuperuser
```

### Finally, RUN SERVER
```bash
python manage.py runserver
```
