#!/usr/bin/env python3

import uuid
from datetime import datetime
"""
Base model for new project
"""
class BaseModel:
    """
    define constructor 
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        
    def __str__(self):
        return f" BaseModel {self.id} {self.__dir__}"
    
    def save(self):
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    def to_dict(self):
        return {
                    "id": self.id,
                    "created_at": self.created_at,
                    "updated_at": self.updated_at,
                    "__class__": self.__class__.__name__
                }