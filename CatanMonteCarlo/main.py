from random import shuffle, choice, randint
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
import numpy as np

SCALE = 3
RESOURCE = ['brick', 'lumber', 'wool', 'grain', 'ore', 'desert']
RESOURCE_TILES = [
    'brick', 'brick', 'brick',
    'lumber', 'lumber', 'lumber', 'lumber',
    'wool', 'wool', 'wool', 'wool',
    'grain', 'grain', 'grain', 'grain',
    'ore', 'ore', 'ore',
    'desert'
    ]
DICE_SYMBOLS = {2:"*", 3:"**", 4:"***", 5:"****", 6:"*****", 7:"", 8:"*****", 9:"****", 10:"***", 11:"**", 12:"*"}
RESOURCE_SHORT = dict(zip(['b', 'l', 'w', 'g', 'o', 'd'], RESOURCE))
RESOURCE_COLOUR = dict(zip(RESOURCE, ['#CC6600', '#009900', '#CCFF99', '#FFFF99', '#C0C0C0', '#000000']))
DICE_NUMBERS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 7]
HEX_COORDS = [
    [0,2,-2],
    [1,1,-2],
    [2,0,-2],
    [-1,2,-1],
    [0,1,-1],
    [1,0,-1],
    [2,-1,-1],
    [-2,2,0],
    [-1,1,0],
    [0,0,0],
    [1,-1,0],
    [2,-2,0],
    [-2,1,1],
    [-1,0,1],
    [0,-1,1],
    [1,-2,1],
    [-2,0,2],
    [-1,-1,2],
    [0,-2,2]
]

HEX_COORDS = [[a * 3 for a in coord] for coord in HEX_COORDS]

VERTEX_VECTORS=[[ 2/3, -1/3, -1/3], [-2/3,  1/3,  1/3], [-1/3,  2/3, -1/3], [ 1/3, -2/3,  1/3], [-1/3, -1/3,  2/3], [ 1/3,  1/3, -2/3]]
VERTEX_VECTORS = [[int(a * SCALE) for a in coord] for coord in VERTEX_VECTORS]

VERTEX_COORDS=[]

for hex in HEX_COORDS:
      for vert in VERTEX_VECTORS:
          v = [sum(x) for x in zip(hex, vert)]
          if v in VERTEX_COORDS:
              continue
          else:
             VERTEX_COORDS.append(v)

def cube_to_doubleheight(cube):
    y = -cube[2]
    x = -(2 * cube[1] + cube[2]) * np.sqrt(1/3)
    return(x, y)
             

def random_placement():
    """
    Returns a placement dictionary.
    """
    tile_index = list(range(0, 19, 1))
    hc = HEX_COORDS[:-1]
    rt = RESOURCE_TILES[:-1]
    shuffle(rt)
    dn = DICE_NUMBERS[:-1]
    shuffle(dn)
    placement = dict(zip(tile_index, hc))
    placement = {ti: {
        "hex_coords" : coord,
        "resource" : r,
        "dice_number" : d} for ti, coord, r, d in zip(tile_index, hc, rt, dn)}
    placement[tile_index[-1]] = {
        'hex_coords' : HEX_COORDS[-1],
        'resource' : RESOURCE_TILES[-1],
        'dice_number' : DICE_NUMBERS[-1]
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
    hc = HEX_COORDS
    l = string.split("-")
    dn = [int(s[:-1]) for s in l]
    rt = [RESOURCE_SHORT[s[-1]] for s in l]

    placement = {ti:{
        "hex_coords" : coord,
        "resource" : resource,
        "dice_number" : d
    } for ti, coord, resource, d in zip(tile_index, hc, rt, dn)}
    placement = list(placement.values())
    return(placement)


class HexTile:
    def __init__(self, coordinates, resource, dice_number):
        self.coordinates = coordinates
        self.dice_number = dice_number
        self.resource = resource
        self.vertex = self.get_vertex()
        self.resource_count = 0
    def get_vertex(self):
        vertex_combinations = [[2/3, -1/3, -1/3], [-2/3,  1/3,  1/3], [-1/3,  2/3, -1/3], [ 1/3, -2/3,  1/3], [-1/3, -1/3,  2/3], [ 1/3,  1/3, -2/3]]
        vertex_combinations = [[int(a * SCALE) for a in l] for l in vertex_combinations]
        vertex = []
        for vc in vertex_combinations:
            vertex.append([sum(x) for x in zip(self.coordinates, vc)])
        return(vertex)
    def check_dice_roll(self, dice_roll_list):
        self.resource_count += dice_roll_list.count(self.dice_number)
    def vertex_result(self, vertex_coords):
        if vertex_coords in self.vertex:
            result = {
                "resource" : self.resource,
                "resource_count" : self.resource_count
            }
            return(result)

class Vertex:
    def __init__(self, vertex_coords):
        self.vertex_coords = vertex_coords
        self.resource_count = {
            "lumber" : 0,
            "brick" : 0,
            "wool": 0,
            "grain" :0,
            "ore": 0,
            "desert": 0
        }
    def check_hex(self, HexTile):
        if self.vertex_coords in HexTile.vertex:
            self.resource_count[HexTile.resource] += HexTile.resource_count
        self.resource_count['total'] = sum([self.resource_count[r] for r in ['lumber', 'brick', 'wool', 'grain', 'ore']])
    
def show_board(hexes, vertices, n):
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    circle_poly = Circle((0, 0), 10, color = 'lightblue', alpha = 0.2)
    ax.add_patch(circle_poly)
    for hex in hexes:
        x, y = cube_to_doubleheight(hex.coordinates)
        hex_poly = RegularPolygon((x, y), numVertices=6, radius= 2*0.9, color = RESOURCE_COLOUR[hex.resource],
                            orientation = np.radians(60), alpha = 1)
        ax.add_patch(hex_poly)
        if hex.dice_number in [6, 8]:
            text_colour = 'red'
        else:
            text_colour = 'black'
        ax.text(x, y+0.1*SCALE, str(hex.dice_number), ha = 'center', va = 'center', color = text_colour)
        ax.text(x, y-0.1*SCALE, DICE_SYMBOLS[hex.dice_number], ha = 'center', va = 'center', color = text_colour)

    totals = sorted([vertex.resource_count['total'] for vertex in vertices], reverse = True)
    highlight_threshold = totals[5]
    
    for vertex in vertices:
        x, y = cube_to_doubleheight(vertex.vertex_coords)
        ax.scatter(x, y, alpha = vertex.resource_count['total']/n, color = 'black')
        if vertex.resource_count['total'] >= highlight_threshold:
            ax.text(x, y, str(vertex.resource_count['total']), weight='bold')
        else:
            ax.text(x, y, str(vertex.resource_count['total']))
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
    hexes = [HexTile(p['hex_coords'], p['resource'], p['dice_number']) for p in placement]
    vertices = [Vertex(vc) for vc in VERTEX_COORDS]
    dice_roll_list = roll_dice(n)
    for tile in hexes:
        tile.check_dice_roll(dice_roll_list)
    for v in vertices:
        for tile in hexes:
            v.check_hex(tile)

    show_board(hexes, vertices, n)

if __name__ == "__main__":
    simulate(string_placement(), 100)