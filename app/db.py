import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

# Column(Integer, Sequence('module_id_seq'), primary_key=True)

class Module(Base):
    __tablename__ = 'modules'

    _id = Column(String(), primary_key=True)
    _label = Column(String())
    _hatch_status = Column(Integer())
    _automatic = Column(String())


class Sensor(Base):
    __tablename__ = 'sensors'

    _id = Column(String(), primary_key=True)
    _label = Column(String())
    _type = Column(String())


class Setting(Base):
    __tablename__ = 'settings'

    _id = Column(String(), primary_key=True)
    _label = Column(String())
    _type = Column(String())
    _subtype = Column(String())
    _min = Column(Integer())
    _max = Column(Integer())

Base.metadata.create_all(engine)