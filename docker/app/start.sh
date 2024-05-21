#!/bin/bash

if [[ -n $CELERY_MODE ]]; then
    make run-worker
else
    make run-bot
fi