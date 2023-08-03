#!/bin/bash

set -e

python3 seed_data.py
python3 -m gunicorn app:app
