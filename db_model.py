"""Super Hero API - Data Model

Super Hero DB Model created with ORM SQL Alchemy.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import declarative
import sqlalchemy
import os

# Envionrment Variables
DB_USER=os.getenv('DB_USER', None)
DB_PASS=os.getenv('DB_PASS', None)
DB_HOST=os.getenv('DB_HOST', 'localhost')
DB_PORT=os.getenv('DB_PORT', 5432)
DB_NAME=os.getenv('DB_NAME', 'super_hero_db')
DB_SCHEMA=os.getenv('DB_SCHEMA', 'sqlite')

# Postgres Configuration
conn_str = '%s:%d/%s' % (DB_HOST, int(DB_PORT), DB_NAME)
if DB_USER and DB_PASS:
    conn_str = '%s:%s@%s' % (DB_USER, DB_PASS, conn_str)

engine = sqlalchemy.create_engine('%s://%s' % (DB_SCHEMA, conn_str))
SessionModule = sessionmaker(bind=engine)
conn = engine.connect()
session = SessionModule(bind=conn)
Base = sqlalchemy.ext.declarative.declarative_base()

class SuperHeros(Base):
    __tablename__ = 'superheros'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

class PowerStats(Base):
    __tablename__ = 'powerstats'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    intelligence = sqlalchemy.Column(sqlalchemy.Integer)
    strength = sqlalchemy.Column(sqlalchemy.Integer)
    speed = sqlalchemy.Column(sqlalchemy.Integer)
    durability = sqlalchemy.Column(sqlalchemy.Integer)
    power = sqlalchemy.Column(sqlalchemy.Integer)
    combat = sqlalchemy.Column(sqlalchemy.Integer)

class Biography(Base):
    __tablename__ = 'biography'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    full_name = sqlalchemy.Column(sqlalchemy.String)
    alter_egos = sqlalchemy.Column(sqlalchemy.String)
    place_of_birth = sqlalchemy.Column(sqlalchemy.String)
    first_appearance = sqlalchemy.Column(sqlalchemy.String)
    publisher = sqlalchemy.Column(sqlalchemy.String)
    alignment = sqlalchemy.Column(sqlalchemy.String)

class Aliases(Base):
    __tablename__ = 'aliases'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    alias_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

class Appearance(Base):
    __tablename__ = 'appearance'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    gender = sqlalchemy.Column(sqlalchemy.String)
    race = sqlalchemy.Column(sqlalchemy.String)
    height_imperial = sqlalchemy.Column(sqlalchemy.String)
    height_metric = sqlalchemy.Column(sqlalchemy.String)
    weight_imperial = sqlalchemy.Column(sqlalchemy.String)
    weight_metric = sqlalchemy.Column(sqlalchemy.String)
    eye_colour = sqlalchemy.Column(sqlalchemy.String)
    hair_colour = sqlalchemy.Column(sqlalchemy.String)

class Work(Base):
    __tablename__ = 'work'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    occupation = sqlalchemy.Column(sqlalchemy.String)
    base = sqlalchemy.Column(sqlalchemy.String)

class Connections(Base):
    __tablename__ = 'connections'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    group_affiliation = sqlalchemy.Column(sqlalchemy.String)
    relatives = sqlalchemy.Column(sqlalchemy.String)

class Image(Base):
    __tablename__ = 'image'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.String)


Base.metadata.create_all(engine)