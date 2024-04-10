import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

pygame.display.set_caption("EBAL PP")

fps = 60

Frame_per_sec = pygame.time.Clock()

screen_width = 600
screen_height = 600
speed = 5
score = 0

screen = pygame.display.set_mode((screen_width,screen_height))
screen.fill("White")

font = pygame.font.SysFont("Verdana",60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("GAME OVER",True,"Red")

background = pygame.image.load("road.png")

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(20,40), random.randint(20,40)))
        self.image.fill("Yellow")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-1000, -100)

    def update(self):
        self.rect.y += 5
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-1000, -100)
            self.rect.x = random.randint(0, screen_width - self.rect.width)
    def move(self):
        global score
        self.rect.move_ip(0,speed)
        if (self.rect.top > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width-40), 0)  
 
      def move(self):
        global score
        self.rect.move_ip(0,speed)
        if (self.rect.top > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()  
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < screen_width:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

p1 = Player()
e1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(e1)
all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(e1)
coins = pygame.sprite.Group()
collected_coins = 0

INC_SPEED = pygame.USEREVENT + 1

N = 10

while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if collected_coins >=  N:
              speed += 3
              N+=10   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    screen.blit(background, (0,0))
    scores = font_small.render(str(score), True,"Black")
    screen.blit(scores, (10,10))
    
    if len(coins) < 10:  # Limit the number of coins on the screen
        if random.random() < 0.02:  # Adjust the probability for more or fewer coins
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

    all_sprites.update()
    all_sprites.draw(screen)

    hits = pygame.sprite.spritecollide(p1, coins, True)
    for hit in hits:
        # Handle collision logic here (e.g., increase score)
        collected_coins += 1

    # Render collected coins
    text = font.render(f"Coins: {collected_coins}", True, "White")
    text_rect = text.get_rect()
    text_rect.topright = (screen_width - 10, 10)
    screen.blit(text, text_rect)

    pygame.display.flip()
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(p1, enemies):
          pygame.mixer.Sound('crash.mp3').play()
          time.sleep(0.5)
                    
          screen.fill("Red")
          screen.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    Frame_per_sec.tick(fps)