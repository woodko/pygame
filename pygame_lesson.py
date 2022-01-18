# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


width = 480
height = 600
fps = 60

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 240, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #         self.image = pygame.Surface((50, 40))
        #         self.image.fill(green)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        #         pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.centery = height - 30
        self.speedx = 0
        self.shield = 100

        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

        #показать игрока, если скрыт
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        #временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)

# Моб
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #         self.image = pygame.Surface((30, 40))
        #         self.image.fill(red)
        #         self.image_orig = meteor_img
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #         pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > height + 10
            or self.rect.left < -25
            or self.rect.right > width + 20
        ):
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, 40)
            self.speedy = random.randrange(1, 8)
            # Вращение спрайтов

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            # Центр прямоугольника для ровного вращения
            old_center = self.rect.center
            #  self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


# Пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #         self.image = pygame.Surface((10, 20))
        #         self.image.fill(yellow)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

# Взрыв
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            
# Загрузка мелодий игры (звуки)
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(black)
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    "meteorBrown_big1.png",
    "meteorBrown_med1.png",
    "meteorBrown_med3.png",
    "meteorBrown_small1.png",
    "meteorBrown_small2.png",
    "meteorBrown_tiny1.png",
]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)

font_name = pygame.font.match_font("arial")

#  Отрисовка текста очков
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
# Отрисовка полосы здоровья
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
    


# Цикл игры
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    # Проверка - попадание в моба
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        #newmob()

    # Проверка - не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(
        player, mobs, True, pygame.sprite.collide_circle
    )
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        running = False


    # Рендеринг
    screen.fill(blue)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, width - 100, 5, player.lives, player_mini_img)
    

    # После отрисовки всего переворачиваем экран
    pygame.display.flip()


pygame.quit()
