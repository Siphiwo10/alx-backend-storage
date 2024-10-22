#!/usr/bin/env python3
"""returns the list of school having a specific topic:"""


def schools_by_topic(mongo_collection, topic):
    """Find schools that have the specified topic"""
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
