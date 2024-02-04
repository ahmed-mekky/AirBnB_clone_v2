#!/usr/bin/python3
"""Database Engine"""
from sqlalchemy import create_engine
from os import getenv
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
            Base.metaData.drop_all(self.__engine)

    def all(self, cls=None):
        tmp = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.name}.{obj.id}"
                tmp[key] = obj
        else:
            for classname in classes.keys():
                for obj in self.__session.query(classes[classname]).all():
                    key = f"{obj.__class__.name}.{obj.id}"
                    tmp[key] = obj
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
        print("HI")
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
