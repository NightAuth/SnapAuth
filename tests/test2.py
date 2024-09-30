import pygame
import noise
import numpy as np
import random
import json

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

color1 = (62, 218, 214)
color2 = (55, 202, 236)
color3 = (20, 176, 214)
color4 = (28, 136, 208)
color5 = (23, 89, 141)
colors = [color1, color2, color3, color4, color5]

scale = 50
octaves = 3
persistence = 0.5
lacunarity = 2.0
speed = 0.01

clock = pygame.time.Clock()
time_offset = 0

json_file = 'spot_data.json'

def perlin_position(time_offset):
    x = int((noise.pnoise3(time_offset, 0, 0, octaves=octaves, persistence=persistence, lacunarity=lacunarity) + 0.5) * width)
    y = int((noise.pnoise3(0, time_offset, 0, octaves=octaves, persistence=persistence, lacunarity=lacunarity) + 0.5) * height)
    return x, y

def draw_random_spot(time_offset):
    color = random.choice(colors)
    
    radius = random.randint(20, 50)
    
    position = perlin_position(time_offset)
    
    pygame.draw.circle(screen, color, position, radius)
    
    return {
        "color": color,
        "position": position,
        "radius": radius
    }

def save_spot_to_json(spot_data):
    with open(json_file, 'w') as f:
        json.dump(spot_data, f, indent=4)

def animate_spots():
    global time_offset
    spot_data = []
    
    screen.fill((255, 255, 255))  
    spot = draw_random_spot(time_offset)  
    
    spot_data.append(spot)
    
    save_spot_to_json(spot_data)
    
    pygame.display.flip()
    
    time_offset += speed


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    animate_spots()
    
    # Control the animation speed
    clock.tick(5)  
    
pygame.quit()
