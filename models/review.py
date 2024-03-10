#!/usr/bin/python3
"""This module defines the `Review` class, which represents a user review for
a place in the application.

The `Review` class inherits from the `BaseModel` class and provides data
validation for review data.
"""
from models.base_model import BaseModel


class Review(BaseModel):
    '''This class represents a review submitted by a user for a place in your
        application.

    Attributes:
        place_id (str): The unique identifier of the place being reviewed.
        user_id (str): The unique identifier of the user who wrote the review.
        text (str): The text content of the review itself.Validation rules
        might apply, e.g., minimum length
    '''
    place_id = ""
    user_id = ""
    text = ""
