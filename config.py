import os
from datetime import timedelta
import app


TOKEN_EXPIRES = timedelta(hours=1)

if 'NAMESPACE' in os.environ and os.environ['NAMESPACE'] == 'heroku':
    db_uri = os.environ['DATABASE_URL_TRUE']
    debug_flag = False
else:
    db_path = os.path.join(os.path.dirname(__file__), 'golf-buddy.db')
    db_uri = 'sqlite:///./golf-buddy.db'
    debug_flag = True
SQLALCHEMY_DATABASE_URI = db_uri
JWT_SECRET_KEY = 'my secret key'
JWT_ACCESS_TOKEN_EXPIRES = TOKEN_EXPIRES


"""if 'WEBSITE_HOSTNAME' in os.environ:  # running on Azure: use postgresql
    database = os.environ['DBNAME']  # postgres
    host_root = '.postgres.database.azure.com'
    host = os.environ['golfbuddy'] + host_root  # app-name + root
    user = os.environ['DBUSER']
    password = os.environ['DBPASS']
    port = os.environ.get('DBPORT', '8000')
    db_uri = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    debug_flag = False
else: # when running locally: use sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    debug_flag = True
SQLALCHEMY_DATABASE_URI = db_uri
JWT_SECRET_KEY = 'my secret key'
JWT_ACCESS_TOKEN_EXPIRES = TOKEN_EXPIRES
"""
"""

if "AZURE_POSTGRESQL_CONNECTIONSTRING" in os.environ:
    conn = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
    values = dict(x.split("=") for x in conn.split(' '))
    user = values['user']
    host = values['host']
    database = values['dbname']
    password = values['password']
    db_uri = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    debug_flag = False
else: # when running locally: use sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = f'sqlite:///{db_path}'
    debug_flag = True
SQLALCHEMY_DATABASE_URI = db_uri
JWT_SECRET_KEY = 'my secret key'
JWT_ACCESS_TOKEN_EXPIRES = TOKEN_EXPIRES

"""