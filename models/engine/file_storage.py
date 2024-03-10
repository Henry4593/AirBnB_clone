'''This module provides the FileStorage class for managing persistent storage
    of objects in JSON format. It supports serialization, deserialization, and
    basic object management.
'''
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    '''A class that handles serialization and deserialization of objects
        to/from a JSON file.

        Attributes:
            __file_path (str): The path to the JSON file for storage.
            __objects (dict): An internal dictionary storing objects in memory.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''Returns the dictionary containing all stored objects.

            Returns:
                dict: A dictionary of all stored objects, where keys are
                    object type and ID.
        '''
        return self.__objects

    def new(self, obj):
        '''Adds a new object to the internal storage.

            Args:
                obj: The object to be stored.
        '''
        self.__objects[obj.__class__.__name__ + '.' + str(obj)] = obj

    def save(self):
        '''Serializes the internal objects dictionary to a JSON file.'''
        with open(self.__file_path, 'w+') as json_file:
            json.dump({key: value.to_dict() for key, value in
                      self.__objects.items()}, json_file)

    def reload(self):
        '''Deserializes the JSON file to the internal objects dictionary
            (if it exists).
        '''
        try:
            with open(self.__file_path, 'r') as json_file:
                json_str_dict = json.loads(json_file.read())
                for value in json_str_dict.values():
                    cls = value["__class__"]
                    self.new(eval(cls)(**value))
        except Exception:
            pass
