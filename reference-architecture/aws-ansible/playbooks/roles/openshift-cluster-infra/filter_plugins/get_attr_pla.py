#!/usr/bin/env python
"""
Ansible filter plugin to convert key/val based array
into a key:val dictionary.
Filter supports custom names for key/val.
Author: DevOps <devops@flaconi.de>
Version: v0.1
Date: 2018-05-24
Usage:
var: "{{ an.array | default({}) | get_attr('key', 'val') }}"
"""

import json 

class FilterModule(object):
    def filters(self):
        return {
            'get_attr_pla': filter_list
        }
def filter_list(array, key, value):
    a= ''
    b = {}
    for i in array:
        b['key'] = i[key]
        b['val'] = i[value]
#        a = a + json.dumps(b) + ','
#    return a[:-1]
    return b

