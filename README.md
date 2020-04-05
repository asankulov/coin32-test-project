# Coin32 Test Project

## Prerequisites

* Installed Python3.x
* Installed Docker and docker-compose

## Steps to launch

1. Create `.env` from `.env.example` 
2. Create data and log directories
3. Create `settings_local.py` from `settings_local_example.py`

Then
```
$ docker-compose up -d --build
```
If everything is OK then go to [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)