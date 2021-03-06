#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : conftest.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 9:26:05 pm                       #
# Last Modified : Monday, January 20th 2020, 9:26:52 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
# %%
import os

import numpy as np
from pytest import fixture
import random
import string

from datastudio.core.data import DataStoreFile, DataSourceFile
from datastudio.core.data import DataSet, DataCollection
from datastudio.core.file import File
USECOLS = ["id", "host_id",
            "host_response_rate",
            "host_total_listings_count",
            "host_response_time",
            "host_neighbourhood",
            "host_since",
            "host_is_superhost",
            "host_location",
            "city",
            "zipcode",
            "state",
            "market",
            "neighbourhood_cleansed",
            "accommodates",
            "bed_type",
            "square_feet",
            "beds",
            "room_type",
            "bedrooms",
            "bathrooms",
            "guests_included",
            "property_type",
            "amenities",
            "is_business_travel_ready",
            "maximum_nights",
            "availability_30",
            "minimum_nights",
            "experiences_offered",
            "cleaning_fee",
            "extra_people",
            "price",
            "security_deposit",
            "cancellation_policy",
            "review_scores_cleanliness",
            "review_scores_location",
            "review_scores_communication",
            "review_scores_accuracy",
            "review_scores_rating",
            "review_scores_checkin",
            "number_of_reviews_ltm",
            "reviews_per_month",
            "review_scores_value",
            "license",
            "host_verifications",
            "require_guest_phone_verification",
            "require_guest_profile_picture",
            "host_identity_verified",
            "instant_bookable",
            "requires_license",
            "host_has_profile_pic",
            "last_scraped",
            "calculated_host_listings_count_entire_homes",
            "calculated_host_listings_count_private_rooms",
            "calculated_host_listings_count_shared_rooms",
            "reviews_per_month"]

@fixture(scope="session")
def get_numpy_arrays():
    a = np.arange(0,100)
    b = np.reshape(a, (25,4))
    c = np.logspace(0,100)
    d = np.reshape(c, (5,-1))
    e = np.array([a,b,c,d])
    return a, b, c, d, e

@fixture(scope='session')
def get_text():
    t1 = """Contrary to popular belief, Lorem Ipsum is not simply random.\n"""
    t2 = """Lorem ipsum dolor sit amet.\n"""
    t3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam 
    vitae diam id ipsum lacinia congue eget sed nisi. Nam eget.\n"""
    tl = [t1, t2, t3]
    return t1, tl

@fixture(scope='session')
def get_dfs():
    nash = "./tests/test_data/test_file/nashville.csv"
    sf = "./tests/test_data/test_file/san_francisco.csv"
    fn = File(path=nash, name="Nashville")
    fsf = File(path=sf, name='San Francisco')
    dfn = fn.read(filter=USECOLS)
    dfsf = fsf.read(filter=USECOLS)
    dfs = [dfn, dfsf]
    return dfs

@fixture(scope='function')
def get_datasets():
    source_path = "./tests/test_data/test_file/san_francisco.csv"
    store_path = "./tests/test_data/test_file/san_francisco.xlsx"
    name = 'sf_listings'
    source = DataSourceFile(name, path=source_path)        
    store = DataStoreFile(name, path=store_path)  
    ds1 = DataSet(name=name, datasource=source, datastore=store)     

    source_path = "./tests/test_data/test_file/nashville.csv"
    store_path = "./tests/test_data/test_file/nashville.csv.gz"
    name = 'nashville_listings'
    source = DataSourceFile(name, path=source_path)        
    store = DataStoreFile(name, path=store_path)  
    ds2 = DataSet(name=name, datasource=source, datastore=store)     
    return ds1, ds2

@fixture(scope='session')
def get_arrays():
    """Returns 1, 2, and 3d arrays."""
    a1 = np.random.randint(20,size=100)
    a2 = np.random.normal(10,size=(100))
    a3 = np.random.normal(100,size=(10,10))
    a4 = np.random.randint(10, size=(2,2))
    a5 = np.random.randint(20,size=100)
    return a1, a2, a3, a4, a5

@fixture(scope='session')
def get_X_y():
    """Returns X,y."""
    x = np.random.randint(20,size=(10,10))
    y = np.random.normal(10,size=(10))
    return x,y

@fixture(scope='session')
def get_dict():
    """Returns a randomly generated dictionary."""
    def rstring(length):
            return ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = length)) 
    dict_len = 10
    dictionary = {}
    for i in range(dict_len):
        key = rstring(random.randint(5,20)) 
        dictionary[key] = rstring(random.randint(5,30)) 
    return dictionary 

@fixture(scope='session')
def get_dict_of_lists():
    """Returns a randomly generated dictionary."""
    def rstring(length):
            return ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = length)) 
    dict_len = 5
    dict_depth = 10
    dictionary = {}
    for i in range(dict_len):
        key = rstring(random.randint(5,20)) 
        values = []
        for i in range(dict_depth):
            value = rstring(random.randint(2,10))
            values.append(value)
        dictionary[key] = values
    return dictionary 
