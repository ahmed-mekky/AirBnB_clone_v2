#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import ForeignKey
from models.base_model import BaseModel, Base, String, Column


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
