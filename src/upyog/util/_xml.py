from xml.etree import ElementTree as ET
import re

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