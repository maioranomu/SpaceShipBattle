import pygame
import os

pygame.display.set_caption("Space Battle")
WIDTH, HEIGHT = 1800, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

COLORS = {
    1: (0, 0, 0), # black
    2: (255, 255, 255), # white
    3: (255, 0, 0), # red
    4: (0, 255, 0), # green
    5: (0, 0, 255), # blue
    6: (255, 255, 0) #Yellow 
}
YELLOW = 255, 255, 0
RED = 255, 0, 0

shipW = 50
shipH = 50
TshipW = 300
TshipH = 300

BULLET_SPEED = 12
MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
CRASHED = pygame.USEREVENT + 3

YELLOW_SHIP_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), (shipW, shipH))
yellowX, yellowY = (WIDTH / 2) - 49, HEIGHT - 101

RED_SHIP_SPRITE = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), (shipW, shipH)), False, True)
redX, redY = (WIDTH / 2) - 49, 1

BACKGROUND = pygame.transform.scale((pygame.image.load(os.path.join('Assets', 'space.png'))), (WIDTH, HEIGHT))


def window(red, yellow, red_bullets, yellow_bullets):
    global COLORS
    global angle
    angle = (pygame.math.Vector2(yellow.x - red.x, yellow.y - red.y).angle_to((0, 0))) - 90
    rotated_red_ship = pygame.transform.rotate(RED_SHIP_SPRITE, angle)
    rotated_yellow_ship = pygame.transform.rotate(YELLOW_SHIP_SPRITE, angle)
    WIN.fill(COLORS[1])
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(rotated_yellow_ship, (yellow.x, yellow.y))
    WIN.blit(rotated_red_ship, (red.x, red.y))
    
    # circle_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    # pygame.draw.circle(circle_surface, COLORS[1], (5, 5), 5)
    # WIN.blit(circle_surface, (yellow.x + yellow.width // 2 - 5, yellow.y + yellow.height // 2 - 5))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)  # Corrige aqui
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)  # Corrige aqui
    
    pygame.display.update()



red_bullets = []
def red_move(keys_pressed, red):
    SPEED = 2.5
    
    if keys_pressed[pygame.K_a] and red.x - 2 * SPEED > 0: # RED Left
        red.x -= 2 * SPEED
            
    if keys_pressed[pygame.K_d] and red.x + 2 * SPEED < WIDTH - shipW: # RED Right
        red.x += 2 * SPEED
            
    if keys_pressed[pygame.K_w] and red.y - 2 * SPEED > 0: # RED UP
        red.y -= 2 * SPEED
            
    if keys_pressed[pygame.K_s] and red.y + 2 * SPEED < HEIGHT - shipH: # RED DOWN
        red.y += 2 * SPEED

yellow_bullets = []
def yellow_move(keys_pressed, yellow):
    SPEED = 2.5
    
    if keys_pressed[pygame.K_LEFT] and yellow. x - 2 * SPEED > 0: # YELLOW Left
        yellow.x -= 2 * SPEED
        
    if keys_pressed[pygame.K_RIGHT] and yellow.x + 2 * SPEED < WIDTH - shipW: # YELLOW Right
        yellow.x += 2 * SPEED
         
    if keys_pressed[pygame.K_UP] and yellow.y - 2 * SPEED > 0: # YELLOW UP
        yellow.y -= 2 * SPEED
        
    if keys_pressed[pygame.K_DOWN] and yellow.y + 2 * SPEED < HEIGHT - shipH: # YELLOW DOWN
        yellow.y += 2 * SPEED

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        if bullet.rect.y < 0 or bullet.rect.y > HEIGHT or bullet.rect.x < 0 or bullet.rect.x > WIDTH:
            yellow_bullets.remove(bullet)
        else:
            bullet.rect.x += bullet.velocity.x 
            bullet.rect.y += bullet.velocity.y  
        
        if red.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(RED_HIT))
        
    for bullet in red_bullets:
        if bullet.rect.y < 0 or bullet.rect.y > HEIGHT or bullet.rect.x < 0 or bullet.rect.x > WIDTH:
            red_bullets.remove(bullet)
        else:
            bullet.rect.x += bullet.velocity.x 
            bullet.rect.y += bullet.velocity.y  
        
        if yellow.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            

class Bullet:
    def __init__(self, rect, velocity):
        self.rect = rect
        self.velocity = velocity


def main():    
    red = pygame.Rect(redX, redY, shipW, shipH)
    yellow = pygame.Rect(yellowX, yellowY, shipW, shipH)
    
    run = True
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS: # Red
                    
                    bullet_velocity = pygame.math.Vector2(0, -BULLET_SPEED).rotate(-angle)
                    bullet_rect = pygame.Rect(red.x + (red.width / 2) - 5, red.y + (red.height / 2) - 5, 10, 10)
                    red_bullets.append(Bullet(bullet_rect, bullet_velocity))
                    print(f"Red: {angle}")
                                
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:  # Yellow
                    
                    bullet_velocity = pygame.math.Vector2(0, BULLET_SPEED).rotate(-angle)
                    bullet_rect = pygame.Rect(yellow.x + yellow.width // 2, yellow.y + yellow.height // 2, 10, 10)
                    yellow_bullets.append(Bullet(bullet_rect, bullet_velocity))
                    print(f"Yellow: {angle}")

                
            if event.type == pygame.USEREVENT + 1:
                print("RED WON")
                run = False
                
            if event.type == pygame.USEREVENT + 2:
                print("YELLOW WON")
                run = False
            
            if event.type == pygame.USEREVENT + 3:
                print("Crashed")
                run = False

        keys_pressed = pygame.key.get_pressed()
        
        red_move(keys_pressed, red)
        yellow_move(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
            
        window(red, yellow, red_bullets, yellow_bullets)
    
    pygame.quit()
    

if __name__ == "__main__":
    main()