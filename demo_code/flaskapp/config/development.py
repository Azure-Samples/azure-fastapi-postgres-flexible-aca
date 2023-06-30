import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

dbuser = os.environ["DBSERVER_USER"]
dbpass = os.environ["DBSERVER_PASSWORD"]
dbhost = os.environ["DBSERVER_HOST"]
dbname = os.environ["DBSERVER_DBNAME"]
DATABASE_URI = f"postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}"

TIME_ZONE = "UTC"