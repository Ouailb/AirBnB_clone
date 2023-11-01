#!/usr/bin/env python3

import uuid
from datetime import datetime

"""
Base model for new project
"""


class BaseModel:

    """
        define constructor
        *args, **kwargs arguments for the constructor
    """
    def __init__(self,*args,**kwargs):
        if kwargs:
            if "__class__" in kwargs:
                del kwargs["__class__"]

            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    # Convert the date strings to datetime objects
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
