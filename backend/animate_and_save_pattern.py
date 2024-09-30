import noise.perlin
import pygame
import noise
import numpy as np
import imageio
import time

pygame.init ()

FPS = 30
DURATION = 10

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

white = (255, 255, 255)
black = (0, 0, 0)

scale = 100
octaves = 4
persistence = 0.5
lacunarity = 2.0
speed = 0.5

noise_grid = np.zeros((width, height))

clock = pygame.time.Clock()
time_offset = 0

def generate_perlin_noise(time_offsets):
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
            
            color_value = int((noise_value + 0.5) * 255)
            noise_grid[x][y] = color_value
            
            if color_value > 128:
                pygame.draw.rect(screen, black, (x, y, 1, 1))
            else:
                pygame.draw.rect(screen, white, (x, y, 1, 1))
                

def animate_and_save_pattern(file_path, duration):
    global time_offset
    screen.fill(white)
    
    frames = []
    
    for frame in range(int(duration * FPS)):
        generate_perlin_noise(time_offset)
        pygame.display.flip()
        
        frame_array = pygame.surfarray.array3d(screen)
        frames.append(frame_array)
        
        time_offset += speed
        
        clock.tick(FPS)
        
    imageio.mimsave(file_path, frames, fps=FPS)
    

def run_pattern():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Pattern click, generating 10 - second clip...")
                file_path = 'pattern_output.mp4'
                animate_and_save_pattern(file_path, DURATION)
                print(f"10-sec vid saved")
                
        animate_patterns()
    
    pygame.quit()
    
    
run_pattern()