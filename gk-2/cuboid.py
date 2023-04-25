import numpy as np
from typing import List, Tuple
from os import listdir
from os.path import isfile, join

def load_cuboids(folder_name: str) -> List:
    files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
    return [Cuboid.load_from_file(join(folder_name, f)) for f in files]

class Cuboid:
    def __init__(self):
        super().__init__()
        self.nodes = np.zeros([0,4])
        self.triangles = []
    
    def add_node(self, new_node: Tuple[float, float, float]) -> None:
        self.nodes = np.vstack([self.nodes, np.asarray(new_node+ (1,))])

    def add_edge_to_wall(self, wall_index, new_edge: Tuple[int, int]) -> None:
        for i in new_edge:
            if any([all(self.nodes[j][k] == self.nodes[i][k] for k in range(4)) for j in self.walls[wall_index]]):
                continue
            self.walls[wall_index].append(i)

    def add_triangle(self, new_triangle: Tuple[int, int, int], color: Tuple[int, int, int]) -> None:
        self.triangles.append(Triangle.get_triangle(new_triangle, color))
    
    
    def transform(self, transformation: np.array) -> None:
        self.nodes = self.nodes @ transformation

    @staticmethod
    def load_from_file(file_name: str):
        cuboid = Cuboid()
        i = 0
        colors = []
        color_it = 0
        with open(file_name, 'r') as file:
            for j in range(3):
                color = tuple(int(p) for p  in file.readline().split(','))
                colors.append(color)

            for line in file.readlines():
                if(line == '\n'):
                    color_it = color_it+1
                    continue
                points = [float(p) for p in line.split(',')]
                first_point = tuple(points[:3])
                second_point = tuple(points[3:6])
                third_point = tuple(points[6:])
                cuboid.add_node(first_point)
                cuboid.add_node(second_point)
                cuboid.add_node(third_point)
                cuboid.add_triangle((i, i+1, i+2), colors[int(color_it/2)])
                i = i + 3
        return cuboid
    
class Triangle:
    def __init__(self):
        super().__init__()
        self.points = ()
        self.color = ()
        self.cor = ()
    
    @staticmethod
    def get_triangle(points: Tuple[int, int, int], color: Tuple[int, int, int]):
        triangle = Triangle()
        triangle.points = points
        triangle.color = color
        return triangle
    
    def read_cor(self, cords):
        self.cor = cords

    


    