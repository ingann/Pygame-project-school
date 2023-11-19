import pygame
import os
from random import choice, randint
    
res = 800, 600
fps = 60
monstersize = 32
robot_speed = 300
monster_speed = 400
    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, monsters, *grps):
        super().__init__(*grps)
        self.image = pygame.image.load("robot.png")
        self.state = 'stay'
        self.direction = 'right'
        self.animation_counter = 0
        self.rect = self.image.get_rect(topleft=pos)
        self.monsters = monsters
        self.lives = 3
        self.hitbox = pygame.Rect(0, 0, 30, 20)
        self.hitbox.center = self.rect.center
        self.hitbox.move_ip(-10, -10)
    
    def update(self, dt, events):
        x = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: x -= 1
        if pressed[pygame.K_RIGHT]: x += 1
    
        self.rect.move_ip(x * dt * robot_speed, 0)
        display_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(display_rect)
    
        if x == 1:
            self.direction = 'right'
        if x == -1:
            self.direction = 'left'
        if x == 0:
            new_state = 'stay'
    
        for monster in self.monsters:
            if self.hitbox.colliderect(monster.rect):
                monster.kill()
                self.lives -= 1
        
        self.hitbox.center = self.rect.center
        self.hitbox.move_ip(10 if self.direction == 'left' else -10, -10)
    
class Monsters(pygame.sprite.Sprite):
    def __init__(self, pos, *grps):
        super().__init__(*grps)
        self.image = pygame.image.load("monster.png")
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self, dt, events):
        self.rect.move_ip(0, monster_speed * dt)
        display_rect = pygame.display.get_surface().get_rect()
        if self.rect.top > display_rect.bottom:
            self.kill()
    
    
def main():
    pygame.init()
    pygame.display.set_caption("Avoid monsters")
    screen = pygame.display.set_mode(res)
    dt, clock = 0, pygame.time.Clock()
    sprites = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    player = Player((300, 500), monsters, sprites)
    font = pygame.freetype.SysFont('Arial', 54)
    
    create_monster = pygame.USEREVENT + 1
    pygame.time.set_timer(create_monster, randint(1000, 2000), True)
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == create_monster:
                pygame.time.set_timer(create_monster, randint(1000, 2000), True)
                Monsters((randint(50, 550), -monstersize), monsters, sprites)
            if player.lives == 0:
                main()
    
        color = (25,25,112)
        screen.fill(color)
        font.render_to(screen, (500, 20), f'Lives: {player.lives}', 'black')
        sprites.draw(screen)
        sprites.update(dt, events)
        pygame.display.flip()
        dt = clock.tick(fps) / 1000
    
if __name__ == "__main__":
    main()