#!/bin/bash

set -e

python3 -m flask db upgrade --directory flaskapp/migrations
#python3 -m flask seed
python3 -m gunicorn --reload app:app