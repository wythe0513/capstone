import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Turn off track modifications warning
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Connect to the database
# DONE IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wythenshawe0513@localhost:5432/heroku'