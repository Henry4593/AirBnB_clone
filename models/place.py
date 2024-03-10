#!/usr/bin/python3
"""This module defines the Place class, which represents a place entity within
the application
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """This class represents a place (e.g., rental property, hotel) within the
      application.

    Attributes:
      city_id (str): Foreign key referencing a City model
      user_id (str): Foreign key referencing a User model
      name (str): The name of the place.
      description (str): A description of the place.
      number_rooms (int): The number of rooms in the place
                           (must be a non-negative integer).
      number_bathrooms (int): The number of bathrooms in the place
                               (must be a non-negative integer).
      max_guest (int): The maximum number of guests allowed in the place
                         (must be a non-negative integer).
      price_by_night (int): The price per night for staying at the place
                            (must be a non-negative integer).
      latitude (float): The geographical latitude of the place.
      longitude (float): The geographical longitude of the place.
      amenity_ids (list[str]): A list of amenity IDs referencing the Amenity
                               model (if applicable).
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
