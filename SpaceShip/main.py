import pygame
import os
import random

pygame.mixer.init()
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

BULLET_SPEED = 12
MAX_BULLETS = 4
asteroids = []
time_since_last_asteroid = 0
asteroid_spawn_delay = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
CRASHED = pygame.USEREVENT + 3

YELLOW_SHIP_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), (shipW, shipH))
yellowX, yellowY = (WIDTH / 2) - 49, HEIGHT - 101

RED_SHIP_SPRITE = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), (shipW, shipH)), False, True)
redX, redY = (WIDTH / 2) - 49, 1

BACKGROUND = pygame.transform.scale((pygame.image.load(os.path.join('Assets', 'space.png'))), (WIDTH, HEIGHT))

def window(red, yellow, red_bullets, yellow_bullets, asteroids):
    global angle
    
    angle = (pygame.math.Vector2(yellow.x - red.x, yellow.y - red.y).angle_to((0, 0))) - 90
    rotated_red_ship = pygame.transform.rotate(RED_SHIP_SPRITE, angle)
    rotated_yellow_ship = pygame.transform.rotate(YELLOW_SHIP_SPRITE, angle)
    WIN.fill(COLORS[1])
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(rotated_yellow_ship, (yellow.x, yellow.y))
    WIN.blit(rotated_red_ship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    for asteroid in asteroids[:]: 
        WIN.blit(asteroid["image"], (asteroid["rect"].x, asteroid["rect"].y))
        asteroid["rect"].x -= 2  
        if asteroid["rect"].x < -100:  
            asteroids.remove(asteroid)
        if red.colliderect(asteroid["rect"]):
            pygame.event.post(pygame.event.Event(CRASHED))
            print("Red Crashed")
        if yellow.colliderect(asteroid["rect"]):
            pygame.event.post(pygame.event.Event(CRASHED))
            print("Yellow Crashed")
    
    MAXASTEROIDS = 10
    if len(asteroids) < MAXASTEROIDS:
        if random.randint(0, 1500) < 10:
            randomasteroid = random.randint(1, 2)
            asteroidsizex = random.randint(20, 300)
            asteroidsizey = asteroidsizex
            asteroid_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"asteroid{randomasteroid}new.png")), (asteroidsizex, asteroidsizey))
            asteroid_rect = asteroid_image.get_rect()
            asteroid_rect.x = WIDTH + 300
            asteroid_rect.y = random.randint(0, HEIGHT - asteroid_rect.height)
            asteroid = {"image": asteroid_image, "rect": asteroid_rect}
            asteroids.append(asteroid)
        
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
        
    if yellow.colliderect(red):
        pygame.event.post(pygame.event.Event(CRASHED))
    
            

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
                    bullet_rect = pygame.Rect(red.x + red.width // 2, red.y + red.height // 2, 10, 10)
                    red_bullets.append(Bullet(bullet_rect, bullet_velocity))
                    pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3")).play()
                    print(f"Red: {angle}")
                                
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:  # Yellow
                    
                    bullet_velocity = pygame.math.Vector2(0, BULLET_SPEED).rotate(-angle)
                    bullet_rect = pygame.Rect(yellow.x + yellow.width // 2, yellow.y + yellow.height // 2, 10, 10)
                    yellow_bullets.append(Bullet(bullet_rect, bullet_velocity))
                    pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3")).play()
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
            
        window(red, yellow, red_bullets, yellow_bullets, asteroids)
    
    pygame.quit()
    

if __name__ == "__main__":
    main()
