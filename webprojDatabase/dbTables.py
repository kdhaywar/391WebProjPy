__author__ = 'HenryPabst'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    user_name = Column(String(24), primary_key=True)
    password = Column(String(24))
    date_registered = Column(Date)


class Persons(Base):
    __tablename__ = "persons"

    user_name = Column(String(24), ForeignKey("users.user_name"), primary_key=True)
    first_name = Column(String(24))
    last_name = Column(String(24))
    address = Column(String(128))
    email = Column(String(128), unique=True)
    phone = Column(String(10))


class Groups(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=true)
    user_name = Column(String(24), ForeignKey("users.user_name"), unique=True)
    group_name = Column(String(24), unique=True)
    date_created = Column(Date)


class Group_Lists(Base):
    __tablename__ = "group_lists"

    group_id = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)
    friend_id = Column(String(24), ForeignKey("users.user_name"), primary_key=True)
    date_added = Column(Date)
    notice = Column(String(1024))


class Images(Base):
    __tablename__ = "images"

    photo_id = Column(Integer, primary_key=True)
    owner_name = Column(String(24), ForeignKey("users.user_name"))
    permitted = Column(Integer, ForeignKey("groups.group_id"))
    subject = Column(String(128))
    place = Column(String(128))
    timing = Column(Date)
    description = Column(String(2048))
    thumbnail = Column(BLOB)
    photo = Column(BLOB)


