#!/bin/bash

if [[ -z $CELERY_MODE ]];
then
  alembic upgrade head &&
  python src/main.py
else
  celery -A src.tasks.celery_tasks worker -l info
fi