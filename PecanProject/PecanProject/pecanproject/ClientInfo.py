import sqlalchemy as db
from sqlalchemy.orm import declarative_base

engine = db.create_engine('sqlite:///clientsdata.sqlite', echo = True)
Base= declarative_base()

class ClientInfo(Base): #Class needed to create the database
    __tablename__= 'client_info'
    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String)
    cpu = db.Column(db.Float)
    ram = db.Column(db.Float)
    disk = db.Column(db.Float)
    upTime = db.Column(db.String)
