# new pattern

import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ripple Effect with Randomness')

# Colors
# BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ripple effect parameters
ripple_speed = 2
max_radius = 300
ripple_count = 20

# Class for Ripple object
class Ripple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(0, 30)  # Start with random initial radius
        self.speed = ripple_speed + random.uniform(-1, 1)  # Add randomness to speed
        self.color = [random.randint(100, 255) for _ in range(3)]  # Random color
        self.thickness = random.randint(1, 3)  # Random thickness of ripple

    def draw(self, screen):
        if self.radius < max_radius:
            pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.radius), self.thickness)

    def update(self):
        self.radius += self.speed  # Expand the ripple

# Initialize variables
ripples = []
clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Add a ripple at the position of a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            ripples.append(Ripple(x, y))

    # Draw and update ripples
    for ripple in ripples:
        ripple.draw(screen)
        ripple.update()

    # Remove ripples that are too large
    ripples = [ripple for ripple in ripples if ripple.radius < max_radius]

    # Randomly generate ripples at random positions
    if random.random() < 0.03:  # Random probability of ripple generation
        ripples.append(Ripple(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    # Update the screen
    pygame.display.flip()

    # Frame rate control
    clock.tick(60)

# Quit pygame
pygame.quit()
