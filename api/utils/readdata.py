import json

def read_pickup():
    """
    Returns zones from file

    Returns
    -------
    list
        of dictionary with id location and Borough-Zone merged
    """

    zones = []
    f = open('zone_source/pickup_zones.json')
    data = json.load(f)
    for d in data:
        zones.append({'id': d['LocationID'],'zone':d['Borough'] +'-'+ d['Zone'] })
    f.close()

    return zones

def read_dropoff():
    """
    Returns zones from file

    Returns
    -------
    list
        of dictionary with id location and Borough-Zone merged
    """

    zones = []
    f = open('zone_source/dropoff_zones.json')
    data = json.load(f)
    for d in data:
        zones.append({'id': d['LocationID'],'zone':d['Borough'] +'-'+ d['Zone'] })
    f.close()

    return zones