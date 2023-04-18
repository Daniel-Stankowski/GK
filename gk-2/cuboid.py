import numpy as np
from typing import List, Tuple
from os import listdir, getcwd
from os.path import isfile, join

def load_cuboids(folder_name: str) -> List:
    files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
    return [Cuboid.load_from_file(join(folder_name, f)) for f in files]

class Cuboid:
    def __init__(self):
        super().__init__()
        self.nodes = np.zeros([0,4])
        self.edges = []
        self.walls = [[], [], [], [], [], []]
    
    def add_node(self, new_node: Tuple[float, float, float]) -> None:
        self.nodes = np.vstack([self.nodes, np.asarray(new_node+ (1,))])

    def add_edge(self, new_edge: Tuple[int, int]) -> None:
        self.edges.append(new_edge)

    def add_edge_to_wall(self, wall_index, new_edge: Tuple[int, int]) -> None:
        for i in new_edge:
            if any([all(self.nodes[j][k] == self.nodes[i][k] for k in range(4)) for j in self.walls[wall_index]]):
                continue
            self.walls[wall_index].append(i)
    
    def transform(self, transformation: np.array) -> None:
        self.nodes = self.nodes @ transformation

    @staticmethod
    def load_from_file(file_name: str):
        cuboid = Cuboid()
        i = 0
        with open(file_name, 'r') as file:
            for line in file.readlines():
                points = [float(p) for p in line.split(',')]
                start = tuple(points[:3])
                end = tuple(points[3:6])
                walls = tuple(points[6:])
                cuboid.add_node(start)
                cuboid.add_node(end)
                cuboid.add_edge((i, i+1))
                [cuboid.add_edge_to_wall(int(j), (i, i+1)) for j in walls]
                i = i + 2
        return cuboid


    