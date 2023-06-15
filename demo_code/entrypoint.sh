#!/bin/bash

set -e

gunicorn app:app
