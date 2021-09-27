import CatanMonteCarlo.config as config

class HexTile:
    def __init__(self, coordinates, resource, dice_number):
        self.coordinates = coordinates
        self.dice_number = dice_number
        self.resource = resource
        self.vertex = self.get_vertex()
        self.resource_count = 0
    def get_vertex(self):
        vertex_combinations = [[2/3, -1/3, -1/3], [-2/3,  1/3,  1/3], [-1/3,  2/3, -1/3], [ 1/3, -2/3,  1/3], [-1/3, -1/3,  2/3], [ 1/3,  1/3, -2/3]]
        vertex_combinations = [[int(a * config.SCALE) for a in l] for l in vertex_combinations]
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
    