#!/usr/bin/python3
import pdb
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from eve_sqlalchemy.validation import ValidatorSQL
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property

Base = declarative_base()

class days(Base): #Hours per day when the screen will be on
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hours = Column(String(24))

class clock_on(Base): #When to display the hour on top of the photo
    __tablename__ = 'clock_on'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hours = Column(String(24))

class commands(Base): #send command and get respond from the display
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    command = Column(String(99))
    respond = Column(String(99))

class state(Base): #varios info about state
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String(99))

class config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key=Column(String(23))     
    value=Column(String(23))       # address to ping 


SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://frame@localhost/frame',
    'RESOURCE_METHODS': ['GET','POST','DELETE'],
    'ITEM_METHODS': ['GET','PUT','DELETE','PATCH'],
    'RETURN_MEDIA_AS_URL': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'DOMAIN': DomainConfig({
        'state': ResourceConfig(state),
        'clock_on': ResourceConfig(clock_on),
        'commands': ResourceConfig(commands),
        'config': ResourceConfig(config),
        'days': ResourceConfig(days)
    }).render()
}

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

# using reloader will destroy in-memory sqlite db
app.run(debug=True, use_reloader=False, host='0.0.0.0')
