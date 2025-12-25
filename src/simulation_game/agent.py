import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 5
SPEED = 2

# Colors
COLOR_S = (50, 150, 255) # Blue
COLOR_I = (255, 50, 50)  # Red
COLOR_R = (50, 200, 50)  # Green

class Agent:
    def __init__(self, x, y, state="S"):
        self.x = x
        self.y = y
        self.state = state # S, I, R
        
        # Random velocity
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * SPEED
        self.vy = math.sin(angle) * SPEED
        
        self.recovery_timer = 0
        self.recovery_duration = 300 # frames (e.g. 5 seconds at 60fps)

    def move(self, speed_factor=1.0):
        self.x += self.vx * speed_factor
        self.y += self.vy * speed_factor
        
        # Bounce off walls
        if self.x < RADIUS:
            self.x = RADIUS
            self.vx *= -1
        elif self.x > WIDTH - RADIUS:
            self.x = WIDTH - RADIUS
            self.vx *= -1
            
        if self.y < RADIUS:
            self.y = RADIUS
            self.vy *= -1
        elif self.y > HEIGHT - RADIUS:
            self.y = HEIGHT - RADIUS
            self.vy *= -1

    def update(self, speed_factor=1.0):
        self.move(speed_factor)
        
        # Recovery logic
        if self.state == "I":
            self.recovery_timer += 1 * speed_factor
            if self.recovery_timer >= self.recovery_duration:
                self.state = "R"

    def draw(self, screen):
        color = COLOR_S
        if self.state == "I":
            color = COLOR_I
        elif self.state == "R":
            color = COLOR_R
            
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), RADIUS)

    def check_collision(self, other):
        # Euclidean distance
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.hypot(dx, dy)
        
        if dist < 2 * RADIUS:
            # Simple interaction: Transmit infection
            if self.state == "I" and other.state == "S":
                if random.random() < 0.5: # 50% chance of transmission on contact
                    other.state = "I"
            elif self.state == "S" and other.state == "I":
                if random.random() < 0.5:
                    self.state = "I"
            
            # Simple elastic collision (exchange velocities) - very basic physics
            # To avoid sticking, push them apart slightly? 
            # For simplicity in this "ludic" simulation, we won't do full physics reflection
            # just bounce them randomly or swap velocities
            
            # Swap velocities
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy
            
            # Correct overlap (push apart)
            overlap = 2 * RADIUS - dist
            if dist > 0:
                self.x += (dx / dist) * overlap * 0.5
                self.y += (dy / dist) * overlap * 0.5
                other.x -= (dx / dist) * overlap * 0.5
                other.y -= (dy / dist) * overlap * 0.5
