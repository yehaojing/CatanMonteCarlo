import config

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
    