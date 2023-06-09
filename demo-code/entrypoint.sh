#!/bin/bash

set -e

echo "${0}: running migrations."
python seed_data.py
uvicorn app:app
    --name relecloud \ --bind 0.0.0.0:8000 \
    --timeout 600 \
    --workers 4 \
    --log-level=info
