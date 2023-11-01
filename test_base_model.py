#!/usr/bin/env python3

from models.base_model import BaseModel

test = BaseModel()
print(test.id)
print(test.created_at)
print(test.updated_at)
print(test.save)