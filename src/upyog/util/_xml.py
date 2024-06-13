from xml.etree import ElementTree as ET
import re
from upyog._compat import iteritems, Mapping
from upyog.util.string import safe_decode

def _sanitize_tag(tag):
    tag = re.sub(r'\{.*?\}', '', tag)
    return tag

def _xml2dict(e):
    d = {}

    for child in e:
        cd = _xml2dict(child)

        t  = child.tag
        t  = _sanitize_tag(t)

        if t in d:
            if not isinstance(d[t], list):
                d[t] = [d[t]]
            d[t].append(cd)
        else:
            if t in cd:
                d[t] = cd[t]
            else:
                d[t] = cd

    if e.text:
        t    = _sanitize_tag(e.tag)
        d[t] = e.text

    return d

def xml2dict(s):
    e = ET.fromstring(s)
    return _xml2dict(e)

def _dict2xml(d, e):
    for key, value in iteritems(d):
        if isinstance(value, Mapping):
            sub = ET.SubElement(e, key)
            _dict2xml(value, sub)
        elif isinstance(value, list):
            for v in value:
                sub = ET.SubElement(e, key)
                _dict2xml(v, sub)
        else:
            sub = ET.SubElement(e, key)
            sub.text = str(value)

def dict2xml(d):
    e = ET.Element('root')
    _dict2xml(d, e)
    string = safe_decode(ET.tostring(e))
    return re.sub(r'<root>|</root>', '', string)