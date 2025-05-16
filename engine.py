# Warning: the following program has excessive commenting, not because the code is complex, 
# but to aid my understanding of raycasting and 3D simulation in python as well as for future reference.

import pygame
import math


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()

# map definition 8x8 (1 is wall, 0 is empty space)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

player_x, player_y = 3.0, 3.0  # player position
player_angle = math.pi / 4  # player view angle


def cast_ray(angle, player_x, player_y):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    # step size for the ray
    ray_distance = 0.0
    
    while True:
        ray_distance += 0.1  # move ray forward
        
        # calculate the ray's current position
        ray_x = player_x + cos_a * ray_distance
        ray_y = player_y + sin_a * ray_distance
        
        # check if ray hits a wall
        map_x = int(ray_x)
        map_y = int(ray_y)
        
        if game_map[map_y][map_x] == 1:  # wall hit
            return ray_distance
            
        if ray_distance > 20:  # avoid infinite loop (max ray length)
            break
        
    return None  # no hit


def draw_game():
    for column in range(WIDTH):
        # calculate the angle for each vertical slice
        angle = player_angle - math.pi /6 + (column / WIDTH) * (math.pi / 3)
        
        # cast the ray and get the distance
        ray_distance = cast_ray(angle, player_x, player_y)
        
        if ray_distance is not None:
            # calculate the height of the wall based on the distance
            wall_height = HEIGHT / (ray_distance + 0.0001)
            color = (255, 255 - int(ray_distance *10), 0)  # simple color shading
            
            # draw the wall slice
            pygame.draw.rect(screen, color, (column, HEIGHT // 2 - int(wall_height // 2), 1, int(wall_height)))
    
    
def main():
    global player_x, player_y, player_angle
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # handle player movement here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: player_x += math.cos(player_angle) * 0.1
        if keys[pygame.K_a]: player_x -= math.cos(player_angle) * 0.1
        if keys[pygame.K_s]: player_y -= math.sin(player_angle) * 0.1
        if keys[pygame.K_w]: player_y += math.sin(player_angle) * 0.1
        if keys[pygame.K_LEFT]: player_angle -= 0.05
        if keys[pygame.K_RIGHT]: player_angle += 0.05
        
        # TODO fix player movement with new logic
        
        draw_game()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    

if __name__ == '__main__':
    main()
