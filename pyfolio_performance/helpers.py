import xml.etree.ElementTree as ElementTree

def printXml(xml):
    if xml == None:
        print("No xml given")
        return
    print(ElementTree.tostring(xml, encoding='utf8', method='xml'))

def resolveXmlReference(entry, reference):
    if len(reference) == 0:
        return entry
    if len(reference)==2 and reference == "..":
        return Portfolio.parent_map[entry]
    if reference[:3] == "../":
        return resolveXmlReference(Portfolio.parent_map[entry], reference[3:])
    return entry.find(reference)


from .classPortfolio import *