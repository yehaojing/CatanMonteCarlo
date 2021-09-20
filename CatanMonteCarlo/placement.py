from random import shuffle
import config

def string_placement(string = '4l-11w-12b-8g-3o-6b-9g-5w-10g-11g-5l-10l-7d-9w-4l-8w-2o-6b-3o'):
    """
    Returns a placement dictionary based on input string.
    """
    tile_index = list(range(0, 19, 1))
    hc = config.HEX_COORDS
    l = string.split("-")
    dn = [int(s[:-1]) for s in l]
    rt = [config.RESOURCE_SHORT[s[-1]] for s in l]

    placement = {ti:{
        "config.HEX_COORDS" : coord,
        "resource" : resource,
        "dice_number" : d
    } for ti, coord, resource, d in zip(tile_index, hc, rt, dn)}
    placement = list(placement.values())
    return(placement)

def random_placement():
    RESOURCE_SHORT = dict((v,k) for k,v in config.RESOURCE_SHORT.items())
    rt = [RESOURCE_SHORT[rt] for rt in config.RESOURCE_TILES[:-1]]
    shuffle(rt)
    dn = config.DICE_NUMBERS[:-1]
    shuffle(dn)
    desert = str(config.DICE_NUMBERS[-1]) + RESOURCE_SHORT[config.RESOURCE_TILES[-1]]
    s =[str(d) + r for r, d in zip(rt, dn)]
    s.append(desert)
    shuffle(s)
    s2 = '-'.join(s)
    return(string_placement(s2))