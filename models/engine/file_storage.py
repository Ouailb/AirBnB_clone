#!/usr/bin/env python3
import json

"""
    FileStorage class manage getting and storing data in json file
"""


class FileStorage:

    """"
        private class attributes file path with objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return all data"""
        return FileStorage.__objects

    def new(self, obj):
        """new object"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """"store data in json file"""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    @staticmethod
    def get_class(class_name):
        if class_name == "BaseModel":
            from models.base_model import BaseModel
            return BaseModel
        elif class_name == "User":
            from models.user import User
            return User
        elif class_name == "Amenity":
            from models.amenity import Amenity 
            return Amenity
        elif class_name == "City":
            from models.city import City
            return City 
        elif class_name == "Place":
            from models.place import Place
            return Place
        elif class_name == "Review":
            from models.review import Review
            return Review
        elif class_name == "State":
            from models.state import State
            return State

    @classmethod
    def count(cls, class_name):
        """Count the number of instances of a specific class."""
        count = 0
        for key in cls.__objects:
            if key.startswith(class_name + "."):
                count += 1
        return count
    def reload(self):
        """reload the opening json file and get data"""
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split(".")
                    class_obj = self.get_class(class_name)
                    new_obj = class_obj(**value)
                    self.__objects[key] = new_obj
        except FileNotFoundError:
            pass
