#!/usr/bin/env bash

PIPENV_DIR=$(pipenv --venv)
export PIPENV_DIR
# shellcheck disable=SC1090
source "${PIPENV_DIR}/bin/activate"
echo "0 1 * * * cd ~/src/django-apps/coin32-test-project && source ${PIPENV_DIR}/bin/activate && python manage.py clean_db" > clean_db_cron_job
crontab clean_db_cron_job

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000