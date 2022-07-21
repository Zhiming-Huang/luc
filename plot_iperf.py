#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 19:45:17 2022

@author: zhiming
"""

import pandas as pd

import json

with open("test_results1.json") as jsonfile:
    data = json.load(jsonfile)
    
for interval in data["intervals"]:
    
    