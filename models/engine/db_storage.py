#!/usr/bin/python3
"""Database Engine"""
from sqlalchemy import create_engine, except_
from os import getenv
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity

classes = {
    "City": City,
    "State": State,
    "Place": Place,
    "Review": Review,
    "Amenity": User,
    "User": Amenity,
}


class DBStorage:
    """Main Class for the engine"""

    __engine = None
    __session = None

    def __init__(self) -> None:
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        tmp = {}
        if cls is not None:
            for obj in self.__session.query(classes[cls]).all():
                key = f"{obj.__class__.name}.{obj.id}"
                tmp[key] = obj
        else:
            print("HIIIIIIIIII")
            for classname in classes:
                try:
                    for obj in self.__session.query(classname).all():
                        key = f"{obj.__class__.name}.{obj.id}"
                        tmp[key] = obj
                except sqlalchemy.exc.ArgumentError:
                    pass
        return tmp

    def new(self, obj):
        self.__session.add(obj)
        self.save()

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
