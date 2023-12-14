import pygame
from random import randint

resolution = (1200, 900)
fps = 60
monster_size = 32
robot_speed = 300
monster_speed = 700

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, monsters, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("robot.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.monsters = monsters
        self.lives = 3
        self.hitbox = pygame.Rect(0, 0, 30, 20)
        self.hitbox.center = self.rect.center
        self.hitbox.move_ip(-10, -10)
        self.max_y = resolution[1] - self.rect.height  

    def update(self, dt):
        # Movement handling
        x = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: x -= 1
        if pressed[pygame.K_RIGHT]: x += 1

        self.rect.move_ip(x * dt * robot_speed, 0)
        display_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(display_rect)

        
        if self.rect.bottom > resolution[1]: 
            self.rect.bottom = resolution[1]
        elif self.rect.top < resolution[1] - self.rect.height:  
            self.rect.top = resolution[1] - self.rect.height

        # Collisions with monsters 
        for monster in self.monsters:
            if self.hitbox.colliderect(monster.rect):
                monster.kill()
                self.lives -= 1

        self.hitbox.center = self.rect.center
        self.hitbox.move_ip(10 if x == -1 else -10, -10)

class Monsters(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("monster.png")
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self, dt):
        self.rect.move_ip(0, monster_speed * dt)
        display_rect = pygame.display.get_surface().get_rect()
        if self.rect.top > display_rect.bottom:
            self.kill()

# Game Over 
def game_over(screen):
    font = pygame.freetype.SysFont('freemono', 32)
    game_restart = False 
    while not game_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Retry
                    game_restart = True 
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:  # Exit
                    pygame.quit()
                    exit()

        screen.fill((0, 0, 0))
        text_surface, _ = font.render("Game Over", pygame.Color("red"))
        text_width, text_height = text_surface.get_size()
        screen.blit(text_surface, ((resolution[0] - text_width) // 2, (resolution[1] - text_height) // 2 - 50))

        retry_text_surface, _ = font.render("Press R to Retry or E to Exit", pygame.Color("white"))
        retry_text_width, retry_text_height = retry_text_surface.get_size()
        screen.blit(retry_text_surface, ((resolution[0] - retry_text_width) // 2, (resolution[1] - retry_text_height) // 2 + 50))

        pygame.display.flip()

    return game_restart 

# Main Function
def main():
    pygame.init()
    pygame.display.set_caption("Avoid monsters")
    screen = pygame.display.set_mode(resolution)
    dt, clock = 0, pygame.time.Clock()
    sprites = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    player = Player((300, 500), monsters, sprites)
    font = pygame.freetype.SysFont('freemono', 54)

    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, resolution)

    # Timer for monster creation
    create_monster = pygame.USEREVENT + 1
    pygame.time.set_timer(create_monster, randint(500, 1000), True)  

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == create_monster:
                pygame.time.set_timer(create_monster, randint(500, 1000), True)
                for _ in range(3):
                    Monsters((randint(0, resolution[0] - monster_size), -monster_size), monsters, sprites)
            if player.lives == 0:
                if not game_over(screen):
                    pygame.quit()
                    exit()
                else:
                    player.lives = 3
                    monsters.empty()
                    pygame.time.set_timer(create_monster, randint(500, 1000), True) 

        # Display
        screen.blit(background, (0, 0))
        font.render_to(screen, (500, 20), f'Lives: {player.lives}', 'black')
        sprites.draw(screen)
        sprites.update(dt)
        pygame.display.flip()
        dt = clock.tick(fps) / 1000

if __name__ == "__main__":
    main()
