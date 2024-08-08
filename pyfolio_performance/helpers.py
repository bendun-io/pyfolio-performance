# import xml.etree.ElementTree as ElementTree

# def printXml(xml):
#     if xml == None:
#         print("No xml given")
#         return
#     print(ElementTree.tostring(xml, encoding='utf8', method='xml'))

# def resolveXmlReference(entry, reference):
#     if len(reference) == 0:
#         return entry
#     if len(reference)==2 and reference == "..":
#         return Portfolio.parent_map[entry]
#     if reference[:3] == "../":
#         return resolveXmlReference(Portfolio.parent_map[entry], reference[3:])
#     return entry.find(reference)

def combinePaths(absolute, relative):
    absoluteSplit = absolute.split("/")
    relativeSplit = relative.split("/")
    
    toRemove = 0
    for i in range(len(relativeSplit)):
        if relativeSplit[i] == "..":
            toRemove += 1
        else:
            break

    absoluteSplit = absoluteSplit[:-toRemove]
    relativeSplit = relativeSplit[toRemove:]
    return "/".join(absoluteSplit + relativeSplit)

def copy_from(self, other):
    if not isinstance(other, self.__class__):
        raise ValueError("Can only copy attributes from an instance of the same class")
        
    self.__dict__.update(other.__dict__)

import json
class MyCustomClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Transaction):
            return obj.to_dict()
        elif isinstance(obj, Account):
            return str(obj)#.content.to_dict()
        elif isinstance(obj, Depot):
            return obj.content
        return super().default(obj)

from .classPortfolio import *