#!/usr/bin/env python3
"""inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document into the collection with the
    provided kwargs"""
    new_school_id = mongo_collection.insert_one(kwargs).inserted_id
    return new_school_id
