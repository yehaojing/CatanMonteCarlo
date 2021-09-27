from random import randint

import CatanMonteCarlo.config as config
from CatanMonteCarlo.objects import HexTile, Vertex
from CatanMonteCarlo.utils import show_board

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
