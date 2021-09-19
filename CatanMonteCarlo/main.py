from random import shuffle, choice, randint
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
import numpy as np

import config
from hextile import HexTile
from vertex import Vertex

def cube_to_doubleheight(cube):
    y = -cube[2]
    x = -(2 * cube[1] + cube[2]) * np.sqrt(1/3)
    return(x, y)
             
def random_placement():
    """
    Returns a placement dictionary.
    """
    tile_index = list(range(0, 19, 1))
    hc = config.HEX_COORDS[:-1]
    rt = config.RESOURCE_TILES[:-1]
    shuffle(rt)
    dn = config.DICE_NUMBERS[:-1]
    shuffle(dn)
    placement = dict(zip(tile_index, hc))
    placement = {ti: {
        "config.HEX_COORDS" : coord,
        "resource" : r,
        "dice_number" : d} for ti, coord, r, d in zip(tile_index, hc, rt, dn)}
    placement[tile_index[-1]] = {
        'config.HEX_COORDS' : config.HEX_COORDS[-1],
        'resource' : config.RESOURCE_TILES[-1],
        'dice_number' : config.DICE_NUMBERS[-1]
        }
    desert_index = choice(tile_index)
    placement[desert_index]['resource'], placement[tile_index[-1]]['resource'] = placement[tile_index[-1]]['resource'], placement[desert_index]['resource']
    placement[desert_index]['dice_number'], placement[tile_index[-1]]['dice_number'] = placement[tile_index[-1]]['dice_number'], placement[desert_index]['dice_number']
    placement = list(placement.values())
    return(placement)

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


def show_board(hexes, vertices, n):
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    circle_poly = Circle((0, 0), 10, color = '#0000FF', alpha = 0.2)
    ax.add_patch(circle_poly)
    for hex in hexes:
        x, y = cube_to_doubleheight(hex.coordinates)

        hex_poly_border = RegularPolygon((x, y), numVertices=6, radius= 2, color = 'white',
            orientation = np.radians(60), alpha = 1, zorder = 1)
        hex_poly = RegularPolygon((x, y), numVertices=6, radius= 2*0.9, color = config.RESOURCE_COLOUR[hex.resource],
                            orientation = np.radians(60), alpha = 1, zorder = 1)
        ax.add_patch(hex_poly_border)
        ax.add_patch(hex_poly)
        
        if hex.dice_number in [6, 8]:
            text_colour = 'red'
        else:
            text_colour = 'black'
        ax.text(x, y+0.1*config.SCALE, str(hex.dice_number), ha = 'center', va = 'center', color = text_colour)
        ax.text(x, y-0.1*config.SCALE, config.DICE_SYMBOLS[hex.dice_number], ha = 'center', va = 'center', color = text_colour)

    totals = sorted([vertex.resource_count['total'] for vertex in vertices], reverse = True)
    highlight_threshold = totals[5]
    
    for vertex in vertices:
        x, y = cube_to_doubleheight(vertex.vertex_coords)
        
        if vertex.resource_count['total'] >= highlight_threshold:
            ax.scatter(x, y, color = 'black', zorder = 2)
            ax.text(x, y, str(round(vertex.resource_count['total']/n, 3)), weight='bold')
        else:
            ax.scatter(x, y, color = 'grey', zorder = 2)
            ax.text(x, y, str(round(vertex.resource_count['total']/n, 3)))
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    ax.set_axis_off()

    plt.show()

def roll_dice(n):
    dice_rolls =  []
    for i in range(0, n+1, 1):
        die_1 = randint(1, 6)
        die_2 = randint(1, 6)
        dice_rolls.append(die_1 + die_2)
    return(dice_rolls)

def simulate(placement, n):
    hexes = [HexTile(p['config.HEX_COORDS'], p['resource'], p['dice_number']) for p in placement]
    vertices = [Vertex(vc) for vc in config.VERTEX_COORDS]
    dice_roll_list = roll_dice(n)
    for tile in hexes:
        tile.check_dice_roll(dice_roll_list)
    for v in vertices:
        for tile in hexes:
            v.check_hex(tile)

    show_board(hexes, vertices, n)

if __name__ == "__main__":
    simulate(string_placement('5w-8b-4g-7d-10w-3w-11b-2o-9w-11g-6g-12g-6o-4l-5o-9l-3l-8l-10b'), 100000)