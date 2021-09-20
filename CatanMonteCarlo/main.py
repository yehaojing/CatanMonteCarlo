from utils import cube_to_doubleheight, show_board
from objects import HexTile, Vertex
from placement import string_placement, random_placement
from simulate import simulate

if __name__ == "__main__":
    simulate(random_placement(), 100)