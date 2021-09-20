from utils import cube_to_doubleheight, show_board
from objects import HexTile, Vertex
from placement import string_placement, random_placement
from simulate import simulate

import argparse

def parse_args():
    args = argparse.ArgumentParser()
    placement = args.add_mutually_exclusive_group()
    placement.add_argument("--random_placement", "--r", action = "store_true", help = "random placement")
    placement.add_argument("--string_placement", "--s", help = "string placement")
    args.add_argument("--n_simulations", "--n", help = "number of Monte Carlo simulations to run")
    return(args.parse_args())

def main():
    args = parse_args()
    if args.random_placement:
        placement = random_placement()
    else:
        placement = string_placement(args.string_placement)
    
    simulate(placement, int(args.n_simulations))

if __name__ == "__main__":
    main()