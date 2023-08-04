#!/bin/bash

set -e

python3 fastapi_app/seed_data.py
python3 -m gunicorn fastapi_app:app
