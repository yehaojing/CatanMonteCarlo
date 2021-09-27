import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
import numpy as np

import CatanMonteCarlo.config as config

def cube_to_doubleheight(cube):
    y = -cube[2]
    x = -(2 * cube[1] + cube[2]) * np.sqrt(1/3)
    return(x, y)

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