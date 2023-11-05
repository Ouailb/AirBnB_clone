#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
        Review model
    """

    place_id = ""
    user_id = ""
    text = ""