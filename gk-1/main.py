import pygame
import numpy as np
from typing import Tuple
from cuboid import load_cuboids
import transformations

SCREEN_SIZE = (1200, 800)
EDGE_COLOR = (0,0,0)
EDGE_WIDTH = 1
FOCAL_LIMITS = 20., 500.
FOCAL_STEP = 2.
TRANSLATION_STEP = 10.
ROTATION_STEP = np.radians(2)
BACKGROUND_COLOR = (250,240,230)

focal = 265

def convert_to_plane(point: np.array, view_width: float, view_hight: float, focal: float) -> Tuple[float, float]:
    distance_ratio = focal / point[1]
    x = point[0] * distance_ratio + view_width / 2
    y = view_hight / 2 - point[2] * distance_ratio
    return  x, y

def is_edge_visible(first_point: np.array, second_point: np.array, focal: float) -> bool:
    return (first_point[1] > 0) and (second_point[1] > 0)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("camera")

cuboids = load_cuboids('cuboids')

translation_left = transformations.translation(+TRANSLATION_STEP, 0, 0)
translation_right = transformations.translation(-TRANSLATION_STEP, 0, 0)
translation_backward = transformations.translation(0, +TRANSLATION_STEP, 0)
translation_forward = transformations.translation(0, -TRANSLATION_STEP, 0)
translation_down = transformations.translation(0, 0, +TRANSLATION_STEP)
translation_up = transformations.translation(0, 0, -TRANSLATION_STEP)

rotation_counterclockwise = transformations.rotation(ROTATION_STEP, 'y')
rotation_clockwise = transformations.rotation(-ROTATION_STEP, 'y')
rotation_up = transformations.rotation(ROTATION_STEP, 'x')
rotation_down = transformations.rotation(-ROTATION_STEP, 'x')
rotation_left  = transformations.rotation(ROTATION_STEP, 'z')
rotation_right = transformations.rotation(-ROTATION_STEP, 'z')



on = True
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_MINUS]:
            if focal-FOCAL_STEP > FOCAL_LIMITS[0]:
                focal -= FOCAL_STEP
        if keys[pygame.K_EQUALS]:
            if focal+FOCAL_STEP < FOCAL_LIMITS[1]:
                focal += FOCAL_STEP
        if keys[pygame.K_a]:
            for cuboid in cuboids:
                cuboid.transform(translation_left)
        if keys[pygame.K_d]:
            for cuboid in cuboids:
                cuboid.transform(translation_right)
        if keys[pygame.K_r]:
            for cuboid in cuboids:
                cuboid.transform(translation_up)
        if keys[pygame.K_f]:
            for cuboid in cuboids:
                cuboid.transform(translation_down)
        if keys[pygame.K_w]:
            for cuboid in cuboids:
                cuboid.transform(translation_forward)
        if keys[pygame.K_s]:
            for cuboid in cuboids:
                cuboid.transform(translation_backward)
        if keys[pygame.K_UP]:
            for cuboid in cuboids:
                cuboid.transform(rotation_up)
        if keys[pygame.K_DOWN]:
            for cuboid in cuboids:
                cuboid.transform(rotation_down)
        if keys[pygame.K_LEFT]:
            for cuboid in cuboids:
                cuboid.transform(rotation_left)
        if keys[pygame.K_RIGHT]:
            for cuboid in cuboids:
                cuboid.transform(rotation_right)
        if keys[pygame.K_q]:
            for cuboid in cuboids:
                cuboid.transform(rotation_clockwise)
        if keys[pygame.K_e]:
            for cuboid in cuboids:
                cuboid.transform(rotation_counterclockwise)
        

    screen.fill(BACKGROUND_COLOR)

    for cuboid in cuboids:
        for edge in cuboid.edges:
            first_point = cuboid.nodes[edge[0]]
            second_point = cuboid.nodes[edge[1]]

            if is_edge_visible(first_point, second_point, focal):
                pygame.draw.line(screen, EDGE_COLOR, convert_to_plane(first_point, SCREEN_SIZE[0], SCREEN_SIZE[1], focal), convert_to_plane(second_point, SCREEN_SIZE[0], SCREEN_SIZE[1], focal), EDGE_WIDTH)

    pygame.display.flip()