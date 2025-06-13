from sqlalchemy import Column, Integer, String
from db import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(String)
    location_name = Column(String)
    speaker_name = Column(String)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

class Speaker(Base):
    __tablename__ = "speakers"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bio = Column(String)
