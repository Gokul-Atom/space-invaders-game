import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(f"D:/Game Assets/Spaceship/spaceship_{image + 1}.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(midbottom=(400, 700))
        self.fire_missile = 0
        self.missile_side = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += 3
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 3
        if keys[pygame.K_DOWN] and self.rect.bottom < 800:
            self.rect.y += 3

    def shoot(self):
        self.fire_missile += 0.07
        if int(self.fire_missile):
            self.fire_missile = 0
            player_missile.add(PlayerMissiles(self.rect.left, self.rect.top + 50))
            player_missile.add(PlayerMissiles(self.rect.right, self.rect.top + 50))
            player_missile.add(PlayerMissiles(self.rect.centerx, self.rect.top))

    def update(self):
        self.shoot()
        self.move()


class PlayerMissiles(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load("D:/Game Assets/Fire/missile_1.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

    def fire_missile(self):
        self.rect.y -= 6

    def destroy(self):
        if self.rect.bottom < -10:
            self.kill()

    def update(self):
        self.fire_missile()
        self.destroy()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image_1 = pygame.image.load("D:/Game Assets/Spaceship/enemy_spaceship_1.png").convert_alpha()
        self.image_2 = pygame.image.load("D:/Game Assets/Spaceship/enemy_spaceship_2.png").convert_alpha()
        self.frame_index = randint(0, 1)
        self.frames = [self.image_1, self.image_2]
        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.rotozoom(self.image, 180, 0.5)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def shoot(self):
        if randint(0, 100) == 5:
            enemy_missile.add(EnemyMissiles(self.rect.centerx, self.rect.centery))

    def update(self):
        self.shoot()


class EnemyMissiles(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load("D:/Game Assets/Fire/missile_2.png").convert_alpha(), 180)
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect.inflate_ip(0, -90)

    def fire_missile(self):
        self.rect.y += 6

    def destroy(self):
        if self.rect.top > 810:
            self.kill()

    def update(self):
        self.fire_missile()
        self.destroy()


def collision():
    global pos, game_active
    sprites = pygame.sprite.groupcollide(player_missile, enemy, True, True)
    if sprites:
        for sprite in sprites:
            pos = (sprite.rect[0], sprite.rect[1])

            explosion_animation()
    pygame.sprite.groupcollide(player_missile, enemy_missile, True, True)
    if player.sprite:
        if pygame.sprite.spritecollide(player.sprite, enemy_missile, False):
            pos = player.sprite.rect.center
            player.empty()
            explosion_animation()
            enemy_missile.empty()
            game_active = False
        if not len(enemy.sprites()):
            game_active = False


def explosion_animation():
    global index
    if index >= len(images):
        index = 0
    rect = images[int(index)].get_rect(center=pos)
    screen.blit(images[int(index)], rect)
    index += 0.05
    if index < len(images):
        explosion_animation()


images = []
index = 0
pos = None
for i in range(1, 4):
    image = pygame.image.load(f"D:/Game Assets/Fire/explosion_{i}.png").convert_alpha()
    images.append(image)

font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 100)

text_surf = font.render("Game", False, "white")
text_rect = text_surf.get_rect(center=(400, 200))

# intro screen
game_title_surf = title_font.render("SPACE INVADERS", False, "white")
game_title_rect = game_title_surf.get_rect(center=(400, 200))

start_message_surf = font.render('Press "Space" to destroy invaders', False, "white")
start_message_rect = start_message_surf.get_rect(midbottom=(400, 700))

spaceship_surf = pygame.image.load("D:/Game Assets/Spaceship/spaceship_1.png")
spaceship_surf_1 = pygame.transform.scale2x(spaceship_surf)
spaceship_rect_1 = spaceship_surf_1.get_rect(midright=(350, 400))

spaceship_surf = pygame.image.load("D:/Game Assets/Spaceship/spaceship_2.png")
spaceship_surf_2 = pygame.transform.scale2x(spaceship_surf)
spaceship_rect_2 = spaceship_surf_2.get_rect(midleft=(450, 400))
spaceship_rect_index = 0
spaceship_rects = [spaceship_rect_1, spaceship_rect_2]
spaceship_surfs = [spaceship_surf_1, spaceship_surf_2]

game_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    if game_active:
        screen.blit(text_surf, text_rect)
        screen.fill("#101010")

        player.draw(screen)
        player.update()

        player_missile.draw(screen)
        player_missile.update()

        enemy_missile.draw(screen)
        enemy_missile.update()

        enemy.draw(screen)
        enemy.update()

        collision()

    else:
        screen.fill("#101010")
        screen.blit(game_title_surf, game_title_rect)
        screen.blit(spaceship_surf_1, spaceship_rect_1)
        screen.blit(spaceship_surf_2, spaceship_rect_2)
        screen.blit(start_message_surf, start_message_rect)

        # player
        player = pygame.sprite.GroupSingle()

        # spaceship selection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship_rect_index = 0
        if keys[pygame.K_RIGHT]:
            spaceship_rect_index = 1
        pygame.draw.rect(screen, "red", spaceship_rects[spaceship_rect_index], 5)

        player.add(PlayerShip(spaceship_rect_index))
        player_missile = pygame.sprite.Group()

        # enemy
        enemy = pygame.sprite.Group()
        for x in range(40, 800, 60):
            for y in range(40, 400, 60):
                enemy.add(Enemy(x, y))
        enemy_missile = pygame.sprite.Group()

    pygame.display.update()
    clock.tick(60)
