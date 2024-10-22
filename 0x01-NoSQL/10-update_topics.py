#!/usr/bin/env python3
"""changes all topics of a school document"""


def update_topics(mongo_collection, name, topics):
    """ Update topics of the school document based on the name"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
