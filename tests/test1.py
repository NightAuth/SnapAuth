import noise.perlin
import pygame
import noise
import numpy as np

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height)) 

white = (255, 255, 255)
black = (0, 0, 0)


# Initialize variables for Perlin noise
scale = 100  # Scaling factor for the Perlin noise
octaves = 4  # Number of layers of Perlin noise
persistence = 0.5  # Controls amplitude of noise layers
lacunarity = 2.0  # Controls frequency of noise layers
speed = 0.5  # Speed of animation


noise_grid = np.zeros((width, height))


clock = pygame.time.Clock()
time_offset = 0

def  generate_perlin_noise(time_offset):
    global noise_grid
    
    for x in range(width):
        for y in range(height):
            noise_value = noise.pnoise3(
                x / scale,
                y / scale,
                time_offset,
                octaves = octaves,
                persistence = persistence,
                lacunarity = lacunarity,
                repeatx = width,
                repeaty = height,
                base = 0
            )
            
            color_value = int(noise_value + 0.5) * 255
            noise_grid[x][y] = color_value
            
            
            if color_value > 128:
                pygame.draw.rect(screen, black, (x, y, 1, 1))
            else:
                pygame.draw.rect(screen, white, (x, y, 1, 1))
                

def animate_patterns():
    global time_offset
    
    screen.fill(white)
    generate_perlin_noise(time_offset)
    pygame.display.flip()
    
    time_offset += speed
    
    
    
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    animate_patterns()
    
    clock.tick(30)
    
    
pygame.quit