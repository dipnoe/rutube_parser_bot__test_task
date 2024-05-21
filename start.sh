#!/bin/bash

if [[ -n $CELERY_MODE ]]; then
    make worker-run
else
    make bot-run
fi