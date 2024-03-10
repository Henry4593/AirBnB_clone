#!/usr/bin/python3
"""This module defines the State class, which represents a state entity."""
from models.base_model import BaseModel


class State(BaseModel):
    """This class represents a State entity within the application.

    Attributes:
      name (str): The name of the state
    """
    name = ""
