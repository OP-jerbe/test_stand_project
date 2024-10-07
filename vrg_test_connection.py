# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:27:46 2024

@author: Joshua
"""
import pyvisa

# r'C:\Windows\system32\visa64.dll'
rm = pyvisa.ResourceManager()
vrg_resource = rm.list_resources()[0]
vrg = rm.open_resource(vrg_resource)

query = vrg.query('RQ')
print(query)
vrg.close()