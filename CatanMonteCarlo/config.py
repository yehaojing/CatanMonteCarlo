
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

RESOURCE_COLOUR = dict(zip(RESOURCE, ['#CC6600', '#009900', '#CCFF99', '#FFFF99', '#C0C0C0', '#FF9933']))

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
HEX_COORDS = [[a * 3 for a in coord] for coord in [
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
]]


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

