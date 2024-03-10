'''This module defines the `BaseModel` class, which provides common
functionality for all models in the application. It handles automatic
generation of IDs,timestamps, serialization, and basic string
representation.
'''
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    '''Base class for all models in the application.
    Provides common functionality for managing object creation, updates,
    serialization, and string representation.
    Attributes:
        id (str): Unique identifier for the object (automatically generated).
        created_at (datetime): The datetime when the object was created.
        updated_at (datetime): The datetime when the object was last updated.
    '''
    def __init__(self, *args, **kwargs):
        '''Initializes the base model object.

        Args:
            *args: Optional arguments (not used).
            **kwargs: Keyword arguments for object initialization.
        '''

        d_time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    self.__dict__[key] = datetime.strptime(
                            value, d_time_format)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def save(self):
        '''Updates the `updated_at` attribute with the current datetime
            and saves the object to the storage engine.
        '''
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        '''Returns a dictionary representation of the object.

        Converts the object's attributes to a dictionary, including
        formatted timestamps and the class name.

        Returns:
            dict: A dictionary representation of the object.
        '''
        map_objects = {}
        for key, value in self.__dict__.items():
            if key in ("created_at", "updated_at"):
                map_objects[key] = value.isoformat()
            else:
                map_objects[key] = value
        map_objects["__class__"] = self.__class__.__name__
        return map_objects

    def __str__(self):
        '''Returns a string representation of the object.

        Includes the class name, ID, and all attributes in a human-readable
        format.

        Returns:
            str: String representation of the object.
        '''
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
