#!/usr/bin/python3
"""This module defines the `Amenity` class, which represents an amenity offered
within the application.

Amenity objects can be associated with places (e.g., swimming pool) to provide
details about the place's features.
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """This class represents an amenity offered within your application.

    Attributes:
        name (str): The name of the amenity
    """
    name = ""
