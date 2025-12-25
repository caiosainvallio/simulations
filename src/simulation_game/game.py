import pygame
import random
from .agent import Agent, WIDTH, HEIGHT, COLOR_S, COLOR_I, COLOR_R

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ludic Simulation Lab")
    clock = pygame.time.Clock()
    
    # Initialize Agents
    population_size = 200
    agents = []
    
    # 199 Susceptible, 1 Infected
    for _ in range(population_size - 1):
        x = random.randint(10, WIDTH-10)
        y = random.randint(10, HEIGHT-10)
        agents.append(Agent(x, y, "S"))
        
    # Patient Zero
    agents.append(Agent(WIDTH//2, HEIGHT//2, "I"))
    
    running = True
    speed_factor = 1.0
    font = pygame.font.SysFont("Arial", 18)
    
    # Plotting data
    history_s = []
    history_i = []
    history_r = []
    plot_width = 200
    plot_height = 100
    plot_x = WIDTH - plot_width - 10
    plot_y = 10
    
    while running:
        screen.fill((20, 20, 30)) # Dark background
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    speed_factor = min(5.0, speed_factor + 0.5)
                elif event.key == pygame.K_DOWN:
                    speed_factor = max(0.5, speed_factor - 0.5)

        # Update and Draw Agents
        # Check Collisions (Bubble sort style for simplicity O(N^2) but ok for N=200)
        for i, agent in enumerate(agents):
            agent.update(speed_factor)
            agent.draw(screen)
            
            for j in range(i + 1, len(agents)):
                agent.check_collision(agents[j])
                
        # Count stats
        count_s = sum(1 for a in agents if a.state == "S")
        count_i = sum(1 for a in agents if a.state == "I")
        count_r = sum(1 for a in agents if a.state == "R")
        
        # Update History
        if len(history_s) >= plot_width:
            history_s.pop(0)
            history_i.pop(0)
            history_r.pop(0)
        history_s.append(count_s)
        history_i.append(count_i)
        history_r.append(count_r)
        
        # Draw Overlay Text
        stats_text = f"S: {count_s}  I: {count_i}  R: {count_r}"
        speed_text = f"Speed: {speed_factor:.1f}x (UP/DOWN to change)"
        
        surf_stats = font.render(stats_text, True, (255, 255, 255))
        surf_speed = font.render(speed_text, True, (200, 200, 200))
        
        screen.blit(surf_stats, (10, 10))
        screen.blit(surf_speed, (10, 35))
        
        # Draw Mini Graph
        # Background for graph
        pygame.draw.rect(screen, (0, 0, 0), (plot_x, plot_y, plot_width, plot_height))
        pygame.draw.rect(screen, (100, 100, 100), (plot_x, plot_y, plot_width, plot_height), 1)
        
        if len(history_s) > 1:
            for k in range(1, len(history_s)):
                # Scaling y: height is 100, max val is population_size
                scale_y = plot_height / population_size
                
                # S
                pygame.draw.line(screen, COLOR_S, 
                                 (plot_x + k-1, plot_y + plot_height - history_s[k-1]*scale_y),
                                 (plot_x + k, plot_y + plot_height - history_s[k]*scale_y), 2)
                # I
                pygame.draw.line(screen, COLOR_I, 
                                 (plot_x + k-1, plot_y + plot_height - history_i[k-1]*scale_y),
                                 (plot_x + k, plot_y + plot_height - history_i[k]*scale_y), 2)
                # R
                pygame.draw.line(screen, COLOR_R, 
                                 (plot_x + k-1, plot_y + plot_height - history_r[k-1]*scale_y),
                                 (plot_x + k, plot_y + plot_height - history_r[k]*scale_y), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()
