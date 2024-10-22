#!/usr/bin/env python3
"""Write a Python function that lists all documents in a collection:"""


def list_all(mongo_collection):
    """ Retrieve all documents in the collection"""
    documents = mongo_collection.find()
    document_list = list(documents)
    return document_list
