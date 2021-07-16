# CSV Generator with fake data

Generates CSV file with fake data, which depends on your columns build.

## Description

Dynamic admin panel gives you opportunities to add custom columns for CSV file. Also, possible to add "Separator" and "String Character"

## Getting Started

Project written on Python using Django framework. 

### Dependencies

Database
* DB - PostgreSQL

Need to register and get Keys
* AWS S3
* Redis to Go

Use inside
* Celery
* Gunicorn (u can use your server)

### Installing

* Install Python last version
* Install pip

Move all files from static folder to S3 bucket fodler

In planeks/settings.py:
- Edit DATABASES to connect your database
- Add BROKER_URL
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
### Executing program

If you use CMD
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
For Celery
```
celery -A planeks worker -l info --pool=solor
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Baghili Orkhan

## Version History

* 0.1
    * Initial Release

## License

MIT
