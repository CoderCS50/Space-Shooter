import pygame
from os.path import join
from random import randint



class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        
        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time -self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
                
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # normalize player vector for equal movement speed when multiple direction keys are pressed. 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
            
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            print('fire lasers')
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()    

class Star(pygame.sprite.Sprite):
    def __init__(self,group, surf):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))
    

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
diplay_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center =  (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft =  (20, WINDOW_HEIGHT - 20))

# custom event - meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# game loop
while running:
    # frame rate using dt -- delta time. converted to milliseconds
    dt = clock.tick()/ 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            print('cre')
            
    all_sprites.update(dt)     
    # draw game
    diplay_surface.fill('darkgray')
    all_sprites.draw(diplay_surface)
        
    pygame.display.update()
    
pygame.quit()