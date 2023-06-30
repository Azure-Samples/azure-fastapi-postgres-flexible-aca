#!/bin/bash

set -e

python3 -m flask db upgrade --directory flaskapp/migrations
python3 -m flask seed --filename seed_data.json
python3 -m gunicorn app:app