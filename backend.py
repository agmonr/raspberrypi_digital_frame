#### curl -H "If-Match: b70715c7332dd2bdb6a24a1539b531ffe0166bd1" -H "Content-Type: application/json" -X PATCH -i http://localhost:5000/people/3 -d '{"firstname": "XXXXsaASs"}'



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
    hours = Column(String(23))

class h_display(Base): #When to display the hour on top of the photo
    __tablename__ = 'h_display'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hours = Column(String(23))

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
    root=Column(String(23))               #Images Root folder
    delay=Column(Integer)                 #Daley in sec between images
    yscreenresulation=Column(Integer)
    xscreenresulation=Column(Integer)
    series=Column(Integer)              #Length of image serias
    grayscale=Column(Boolean)           #Show in greyScale
    show_half=Column(Boolean)           #Show hour every 30 minutes
    check_net=Column(Boolean)           #check internet connection
    net_target=Column(String(23))       # address to ping 


SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    'RESOURCE_METHODS': ['GET','POST','DELETE'],
    'ITEM_METHODS': ['GET','PUT','DELETE','PATCH'],
    'RETURN_MEDIA_AS_URL': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'DOMAIN': DomainConfig({
        'state': ResourceConfig(state),
        'h_display': ResourceConfig(h_display),
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

# Insert some example data in the db
if not db.session.query(days).count():
    db.session.add_all([
        days(hours=u'0000001110000000111111'), #monday
        days(hours=u'0000001111111111111111'),
        days(hours=u'0000001110000000111111'),
        days(hours=u'0000001110000000111111'),
        days(hours=u'0000001111111111111111'),
	days(hours=u'0000001111111111111111'),
        days(hours=u'0000001110000000111111')]) #sunday
    db.session.commit()

    db.session.add_all([
        h_display(hours=u'0000000100000000000000'), #monday
	h_display(hours=u'0000000100000000010000'),
	h_display(hours=u'0000000100000000010000'), 
	h_display(hours=u'0000000100000000010000'),
	h_display(hours=u'0000000100000000010000'),
	h_display(hours=u'0000000000000000000000'),
	h_display(hours=u'0000000000000000000000')])
    db.session.commit()

    db.session.add_all([
        config(root=u'/home/Photos/'),
	config(delay=60),
        config(yscreenresulation=1080),
    	config(xscreenresulation=1920),
        config(series=100),
        config(grayscale=0),
        config(show_half=1),
        config(check_net=0),
        config(net_target="8.8.8.8")])   
    db.session.commit()

    db.session.add_all([
        state(image_name="null")])   
    db.session.commit()



# using reloader will destroy in-memory sqlite db
app.run(debug=True, use_reloader=False, host='0.0.0.0')
