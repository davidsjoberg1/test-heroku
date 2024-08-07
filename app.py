from golfbuddy.routes import app
from golfbuddy.models import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0', port=5012)

