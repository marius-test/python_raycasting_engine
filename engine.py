# Warning: the following program has excessive commenting, not because the code is complex, 
# but to aid my understanding of raycasting and 3D simulation in python as well as for future reference.

import pygame  # used for rendering the screen, handling user input, and managing the game loop events
import math  # provides mathematical functions


pygame.init()  # initializes the pygame modules

WIDTH, HEIGHT = 800, 600  # horizontal and vertical resolutions of the game window
screen = pygame.display.set_mode((HEIGHT, WIDTH))  # creates the game window with the specified dimensions
clock = pygame.time.Clock()  # used to control the frame rate of the game loop

# 2D list representing the game map (1 is wall, 0 is empty space)
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

player_x, player_y = 3.0, 3.0  # player's position in the world; using floats for smooth movement, not integers tied to grid cells
player_angle = math.pi / 4  # player's viewing direction in radians; 45 degrees, pointing diagonally


# function to cast a ray at a given angle from the player's current position
def cast_ray(angle, player_x, player_y):
    sin_a = math.sin(angle)  # precompute sine and cosine for the ray angle
    cos_a = math.cos(angle)  # these values tell the direction of the ray in X and Y
    
    # step size for the ray
    ray_distance = 0.0  # start distance of the ray from the player
    
    while True:  # loop until the ray hits a wall or a max range is exceeded
        ray_distance += 0.1  # incrementally extend the ray; the smaller the step, the smoother but slower the raycast
        
        # calculate the ray's current position based on direction and distance
        ray_x = player_x + cos_a * ray_distance
        ray_y = player_y + sin_a * ray_distance
        
        # check if ray hits a wall
        map_x = int(ray_x)  # convert the ray's position into integer map coordinates 
        map_y = int(ray_y)  # to check for wall collisions
        
        if game_map[map_y][map_x] == 1:  # if the ray hits a wall, return how far the ray traveled (used to determine the wall height)
            return ray_distance
            
        if ray_distance > 20:  # prevent infinite loop if the ray never hits anything; 20 is max range
            break
        
    return None  # ray hit nothing


# function to draw one frame of the game world using raycasting
def draw_game():
    for column in range(WIDTH):  # loop once per vertical screen pixel column (simulate a 3D view column-by-column)
        angle = player_angle - math.pi / 6 + (column / WIDTH) * (math.pi / 3) #  calculate the angle of the ray for the current column
        # math.pi / 3 = 60 degrees field of view
        
        ray_distance = cast_ray(angle, player_x, player_y)  # shoot a ray and get distance to the wall
        
        if ray_distance is not None:  # if a wall was hit
            # calculate the height of the wall based on the distance
            wall_height = HEIGHT / (ray_distance + 0.0001)  # inverse relationship; closer wall = taller on screen; +0.0001 avoids division by zero
            color = (255, 255 - int(ray_distance *10), 0)  # simple depth shading; wall gets darker with distance
            
            # draw a 1 pixel wide vertical wall slice centered vertically
            pygame.draw.rect(screen, color, (column, HEIGHT // 2 - int(wall_height // 2), 1, int(wall_height)))
    

# the main function, runs every frame    
def main():
    global player_x, player_y, player_angle  # declares that the player variables will be modified
    
    running = True  # game loop control flag
    while running:  # infinite game loop until the user quits
        # handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # handle player movement here
        keys = pygame.key.get_pressed()  # checks which keys are currently held down
        if keys[pygame.K_w]: player_y += math.sin(player_angle) * 0.1  # moves forward in the direction the player is facing
        if keys[pygame.K_a]: player_x -= math.cos(player_angle) * 0.1  # strafe left
        if keys[pygame.K_s]: player_y -= math.sin(player_angle) * 0.1  # moves backward
        if keys[pygame.K_d]: player_x += math.cos(player_angle) * 0.1  # strafe right
        if keys[pygame.K_LEFT]: player_angle -= 0.05  # rotate player left
        if keys[pygame.K_RIGHT]: player_angle += 0.05  # rotate player right
        
        # TODO fix player movement with new logic
        
        draw_game()  # call the raycasting/drawing functions
        pygame.display.flip()  # refresh the screen with what was drawn
        clock.tick(60)  # 60 frames per second limit
    
    pygame.quit()  # pygame shutdown
    

if __name__ == '__main__':  # runs ONLY the main function if the file is executed
    main()

# TODO add wall collisions
# TODO fix graphics
