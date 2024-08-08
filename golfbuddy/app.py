from golfbuddy import app
from golfbuddy import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import jsonify, request




@app.route('/')
def hello_world():
    return jsonify('hello_world'), 200

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0', port=5012)

