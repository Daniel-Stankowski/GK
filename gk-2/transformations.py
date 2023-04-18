import numpy as np

def translation(dx: float, dy: float, dz: float) -> np.ndarray:
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]], dtype=np.float32
                     )

def rotation(radians: float, axis: str) -> np.ndarray:
    if axis == 'x':
        return np.array([[1, 0, 0, 0],
                         [0, np.cos(radians), -np.sin(radians), 0],
                         [0, np.sin(radians), np.cos(radians), 0],
                         [0, 0, 0, 1]], dtype=np.float32
                         )
    elif axis == 'y':
        return np.array([[np.cos(radians), 0, np.sin(radians), 0],
                         [0, 1, 0, 0],
                         [-np.sin(radians), 0, np.cos(radians), 0],
                         [0, 0, 0, 1]], dtype=np.float32
                         )
    elif axis == 'z':
        return np.array([[np.cos(radians), -np.sin(radians), 0, 0],
                         [np.sin(radians), np.cos(radians), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]], dtype=np.float32
                         )
