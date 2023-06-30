import os

DEBUG = False

if "WEBSITE_HOSTNAME" in os.environ:
    ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]]
else:
    ALLOWED_HOSTS = []

# Configure Postgres database; the full username for PostgreSQL flexible server is
# username (not @server-name).
dbuser = os.environ["DBSERVER_USER"]
dbpass = os.environ["DBSERVER_PASSWORD"]
dbhost = os.environ["DBSERVER_HOST"] + ".postgres.database.azure.com"
dbname = os.environ["DBSERVER_DBNAME"]
DATABASE_URI = f"postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}"