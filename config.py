import os
# DATABASE_URI = 'sqlite:///chitter.db'
# SECRET_KEY = 'asdjasd02309jDs'


DATABASE_URI = os.environ.get(
        'DATABASE_URL').replace('postgres://', 'postgresql://')

SECRET_KEY = os.environ.get(
        'SECRET_KEY')
