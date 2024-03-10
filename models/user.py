#!/usr/bin/python3
"""This module defines the User class, which represents a user entity in the
application.
The User class inherits from the BaseModel class and provides data validation
for user data, including email, password (hashed, not plain text!), first name,
and last name.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class represents a User model for data validation and interacting
    with user data.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.uses hashing for storage
            instead of plain text
        first_name (str): The first name of the user
        last_name (str): The last name of the user
    """
    first_name = ""
    last_name = ""
    email = ""
    password = ""
