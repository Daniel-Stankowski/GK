import pygame
from pygame.locals import *
from sphere_renderer import SphereRenderer
import configparser
import numpy as np

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
draw_light_point = False
BACKGROUND = (0,0,0)

def load_properties_from_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    light_color = tuple(map(int, config.get('LIGHT', 'color').split(',')))
    ambient_intensity = config.getfloat('LIGHT', 'k_a')
    diffuse_intensity = config.getfloat('LIGHT', 'k_d')
    specular_intensity = config.getfloat('LIGHT', 'k_s')
    specular_power = config.getint('LIGHT', 'n')

    return light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power

light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power = load_properties_from_ini()

# define starting position of source of light
light_position = pygame.Vector3(width // 2 - 400, height // 2 - 300, -600)

sphere_position = (width // 2, height // 2, 0)
sphere = SphereRenderer(sphere_position, 200, light_color, ambient_intensity, diffuse_intensity,
                        specular_intensity, specular_power)

# set starting texture
sphere.pearl_texture()

running = True
reload_file = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                light_position.y -= 30
            elif event.key == K_DOWN:
                light_position.y += 30
            elif event.key == K_LEFT:
                light_position.x -= 30
            elif event.key == K_RIGHT:
                light_position.x += 30
            elif event.key == K_w:
                light_position.z += 30
            elif event.key == K_s:
                light_position.z -= 30
            elif event.key == K_l:
                reload_file = True
            elif event.key == K_1:
                sphere.pearl_texture()
            elif event.key == K_2:
                sphere.silver_texture()
            elif event.key == K_3:
                sphere.rubber_texture()
            elif event.key == K_4:
                sphere.gold_texture()
            elif event.key == K_r:
                light_position = pygame.Vector3(width // 2 - 400, height // 2 - 300, -600)
            elif event.key == K_p:
                draw_light_point = not draw_light_point
            if draw_light_point:
                print(light_position)

    if reload_file:
        light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power = load_properties_from_ini()
        sphere.update_light_properties(light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power)
        reload_file = False

    screen.fill(BACKGROUND)
    sphere.set_light_position(light_position)
    sphere.draw(screen)
    if draw_light_point:
        x = np.clip(light_position.x, 0, width)
        y = np.clip(light_position.y, 0, height)
        pygame.draw.circle(screen, (255, 0, 0), (x,y), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
