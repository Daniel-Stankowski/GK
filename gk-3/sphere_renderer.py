import pygame
from math import pi, sin, cos, pow

class SphereRenderer:
    def __init__(self, position, radius, light_color, ambient_intensity, diffuse_intensity, specular_intensity,
                 specular_power):
        self.position = position
        self.radius = radius
        self.light_position = pygame.Vector3(0, 0, 0)
        self.light_color = light_color
        self.ambient_intensity = ambient_intensity #k_a
        self.diffuse_intensity = diffuse_intensity #k_d
        self.specular_intensity = specular_intensity #k_s
        self.specular_power = specular_power

    def set_light_position(self, light_position):
        self.light_position = light_position

    def update_light_properties(self, light_color, ambient_intensity, diffuse_intensity, specular_intensity,
                                specular_power):
        self.light_color = light_color
        self.ambient_intensity = ambient_intensity
        self.diffuse_intensity = diffuse_intensity
        self.specular_intensity = specular_intensity
        self.specular_power = specular_power
    #https://people.eecs.ku.edu/~jrmiller/Courses/672/InClass/3DLighting/MaterialProperties.html
    #http://learnwebgl.brown37.net/10_surface_properties/surface_properties_color.html
    def silver_texture(self):
        self.update_light_properties(light_color=(192, 192, 192), ambient_intensity=0.23125, diffuse_intensity=0.2775,
                                        specular_intensity=0.773911, specular_power=89.6)
        
    def gold_texture(self):
        self.update_light_properties(light_color=(255,215,0), ambient_intensity=0.24725, diffuse_intensity=0.34615,
                                        specular_intensity=0.797357, specular_power=83.2)
        
    def pearl_texture(self):
        self.update_light_properties(light_color=(226, 223, 210), ambient_intensity=0.20725, diffuse_intensity=0.829,
                                        specular_intensity=0.296648, specular_power=11.264)
        
    def rubber_texture(self):
        self.update_light_properties(light_color=(15,15,19), ambient_intensity=1.0, diffuse_intensity=1.0,
                                        specular_intensity=1.0, specular_power=10)

    def draw(self, screen):
        for i in range(360):
            for j in range(180):
                theta1 = i * pi / 180
                theta2 = (i + 2) * pi / 180
                phi1 = j * pi / 180
                phi2 = (j + 2) * pi / 180

                x1 = int(self.radius * sin(phi1) * cos(theta1) + self.position[0])
                y1 = int(self.radius * sin(phi1) * sin(theta1) + self.position[1])
                z1 = int(self.radius * cos(phi1) + self.position[2])

                x2 = int(self.radius * sin(phi1) * cos(theta2) + self.position[0])
                y2 = int(self.radius * sin(phi1) * sin(theta2) + self.position[1])
                z2 = int(self.radius * cos(phi1) + self.position[2])

                x3 = int(self.radius * sin(phi2) * cos(theta1) + self.position[0])
                y3 = int(self.radius * sin(phi2) * sin(theta1) + self.position[1])
                z3 = int(self.radius * cos(phi2) + self.position[2])

                x4 = int(self.radius * sin(phi2) * cos(theta2) + self.position[0])
                y4 = int(self.radius * sin(phi2) * sin(theta2) + self.position[1])
                z4 = int(self.radius * cos(phi2) + self.position[2])

                # calculate normal vector
                normal = pygame.Vector3(x1 - self.position[0], y1 - self.position[1], z1 - self.position[2])
                normal.normalize_ip()

                # calculate light direction
                light_direction = pygame.Vector3(self.light_position[0] - x1, self.light_position[1] - y1, self.light_position[2] - z1)
                light_direction.normalize_ip()

                # calculate view direction
                view_direction = pygame.Vector3(self.position[0] - x1, self.position[1] - y1, self.position[2] - z1)
                view_direction.normalize_ip()

                # calculate reflection direction
                reflection_direction = normal.reflect(light_direction)
                reflection_direction.normalize_ip()

                # calculate ambient component
                ambient = self.ambient_intensity

                # calculate diffuse component
                diffuse = max(normal.dot(light_direction), 0) * self.diffuse_intensity

                # calculate specular component
                specular = pow(max(reflection_direction.dot(view_direction), 0), self.specular_power) * self.specular_intensity

                # calculate final color
                color = (
                    min(int(self.light_color[0] * (ambient + diffuse + specular)), 255),
                    min(int(self.light_color[1] * (ambient + diffuse + specular)), 255),
                    min(int(self.light_color[2] * (ambient + diffuse + specular)), 255)
                )

                pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])
