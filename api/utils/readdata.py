import json

def read_json():
    """
    Returns zones from file

    Returns
    -------
    list
        of dictionary with id location and Borough-Zone merged
    """

    zones = []
    f = open('zone_source/zones.json')
    data = json.load(f)
    for d in data:
        zones.append({'id': d['LocationID'],'zone':d['Borough'] +'-'+ d['Zone'] })
    f.close()

    return zones