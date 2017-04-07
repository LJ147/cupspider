#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by LJ on 2017/3/27
import pprint
from datetime import datetime

from pymongo import MongoClient


def insert_comment(data):
    client = MongoClient('localhost', 27017)
    db = client.novel

    try:
        post_id = db.comment.insert_one(data).inserted_id
    except TypeError, e:
        print e
        print "error"


def insert_comment_with_content(data):
    client = MongoClient('localhost', 27017)
    db = client.novel

    try:
        post_id = db.comment_with_content.insert_one(data).inserted_id
    except:
        # print e
        print "error"


if __name__ == '__main__':
    pass
    # cursor = db.restaurants.find()
