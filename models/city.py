#!/usr/bin/python3
"""This module defines the `City` class, which represents a city entity within
the application.

A `City` object holds information about a city, including its name and the
state it belongs to.
"""
from models.base_model import BaseModel


class City(BaseModel):
    """This class represents a city within your application.

    Attributes:
      state_id (str): The unique identifier of the state the city belongs to.
      name (str): The name of the city.
    """

    state_id = ""
    name = ""
