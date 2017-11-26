import pygame
import random
import math

# colors
BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
YELLOW   = ( 255, 255,  51)

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# images
image_player_r = pygame.image.load("alienGreen_stand.png")
image_player_l = pygame.transform.flip(image_player_r, True, False)
image_player_r_p = pygame.image.load("alienGreen_stand2.png")
image_player_l_p = pygame.transform.flip(image_player_r_p, True, False)
image_monster_l = pygame.image.load("ghost_normal.png")
image_monster_r = pygame.transform.flip(image_monster_l, True, False)
image_bubble = pygame.image.load("darkBlue.png")
image_bubble2 = pygame.image.load("red.png")
image_gems = [ pygame.image.load("blue_gem_1.png"),
               pygame.image.load("cyan_gem_1.png"),
               pygame.image.load("green_gem_1.png"),
               pygame.image.load("orange_gem_1.png"),
               pygame.image.load("pink_gem_1.png"),
               pygame.image.load("yellow_gem_1.png") ]
image_life = pygame.image.load("hud_heartFull.png")
image_bg = [ pygame.image.load("tlo1.jpg"),
             pygame.image.load("tlo2.jpg"),
             pygame.image.load("tlo3.jpg") ]
image_tile = [ pygame.image.load("tile1.png"),
               pygame.image.load("tile2.png"),
               pygame.image.load("tile3.png") ]




class Player(pygame.sprite.Sprite):
  
    def __init__(self, x = 0, y = 0, d = 1):
        
        super().__init__()
        if d == 1:
            self.image = image_player_r.convert()
        else:
            self.image = image_player_l.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_x = 0 # 
        self.v_y = 0
        self.direction = d # d = 1: player facing right, d = 0: player facing left
        self.level = None
        self.walls = pygame.sprite.Group() # walls the player can walk through
        self.walls_side = pygame.sprite.Group() # walls the player can't walk through
        self.bubbles = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.life = 3
        self.score = 0
        self.protected = False
        self.protected_time = 0
        self.sound_splash = pygame.mixer.Sound("shoot.wav")
        self.sound_shoot = pygame.mixer.Sound("shoot.wav")
        self.sound_collect = pygame.mixer.Sound("collect.wav")
        
    def update(self):
        
        self.gravity()
           
        a = self.rect.bottom    
        self.rect.y += self.v_y  
        hits = pygame.sprite.spritecollide(self, self.walls_side, False)
        for block in hits:
            self.rect.top = block.rect.bottom
            self.v_y = 0
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        for block in hits:
            if self.v_y > 0 and a <= block.rect.top:
                self.rect.bottom = block.rect.top
                self.v_y = 0 
        if self.rect.y < 0:
            self.rect.y = 0
            
        self.rect.x += self.v_x
        hits = pygame.sprite.spritecollide(self, self.walls_side, False)
        for block in hits:
            if self.v_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
           
        hits = pygame.sprite.spritecollide(self, self.bubbles, True)
        for h in hits:
            file = open("settings.txt", 'r').readlines()
            if file[0] == '1':
                self.sound_splash.play()
        
        hits = pygame.sprite.spritecollide(self, self.monsters, False)
        for h in hits:
            if h.isinbubble == 1:
                self.score += round((750 - h.t)/5)
                a = random.randrange(-1, 2, 2)
                if a == 1:
                    f = Fruit(random.randrange(40, 950), random.randrange(40, 550), self.walls)
                    for w in self.walls_side:
                        f.walls.add(w)
                    self.fruits.add(f)
                file = open("settings.txt", 'r').readlines()
                if file[0] == '1':
                    self.sound_splash.play()
                h.kill()
            elif not self.protected:
                self.score -= 100
                self.life -= 1
                if self.life != 0:
                    self.rect.x, self.rect.y = self.level.position
                    for m in self.monsters:
                        if m.isinbubble == 1:
                            m.isinbubble = 0
                            if m.direction == 1:
                                m.image = image_monster_r.convert()
                            else:
                                m.image = image_monster_l.convert()
                            m.image.set_colorkey(BLACK)
                self.protected = True
                if self.direction == 1:
                    self.image = image_player_r_p.convert()
                else:
                    self.image = image_player_l_p.convert()
                self.image.set_colorkey(BLACK)
                
        hits = pygame.sprite.spritecollide(self, self.fruits, True)
        for h in hits:
            self.score += 30
            file = open("settings.txt", 'r').readlines()
            if file[0] == '1':
                self.sound_collect.play()                
        
    def gravity(self):
        
        if self.v_y == 0:
            self.v_y = 1
        else:
            self.v_y += 0.3
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = 0
            self.v_y = 0
            self.v_x = 0

    def jump(self):
        platform_hit_list1 = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y += 1
        platform_hit_list2 = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -= 1
        if len(platform_hit_list2) > 0 and len(platform_hit_list1) == 0:
            self.v_y = -9
            
    def left(self):
        self.v_x = -5
        self.direction = -1
        if self.protected == 1:
            self.image = image_player_l_p.convert()
        else:
            self.image = image_player_l.convert()
        self.image.set_colorkey(BLACK)
   
    def right(self):
        self.v_x = 5 
        self.direction = 1
        if self.protected == 1:
            self.image = image_player_r_p.convert()
        else:
            self.image = image_player_r.convert()
        self.image.set_colorkey(BLACK)
        
    def stop(self):
        self.v_x = 0
    
    def shoot(self):
        file = open("settings.txt", 'r').readlines()
        if file[0] == '1':
            self.sound_shoot.play()
        if self.direction == 1:
            return Bubble(self.rect.x+43, self.rect.y, 1)
        else:
            return Bubble(self.rect.x-55, self.rect.y, -1)
 




class Wall(pygame.sprite.Sprite):
        
    def __init__(self, x, y, tile):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



        
        
class Monster(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.direction = random.randrange(-1, 2, 2)
        if self.direction == 1:
            self.image = image_monster_r.convert()
        else:
            self.image = image_monster_l.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_x = 0
        self.v_y = 0
        self.isinbubble = 0
        self.bubbles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.t = 0
        
    def update(self):
        if self.isinbubble == 0: # walking monster
            self.direction *= random.choices([-1, 1], weights = [0.007,0.993])[0]       
            if self.direction == -1:
                self.left()
                self.image = image_monster_l.convert()
            else:
                self.right()
                self.image = image_monster_r.convert()
            self.image.set_colorkey(BLACK)
            
            self.rect.x += self.v_x
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            for block in hits:
                if self.v_x > 0:
                    self.rect.right = block.rect.left
                    self.direction = -1
                else:
                    self.rect.left = block.rect.right
                    self.direction = 1
            
            self.gravity()
            
            self.rect.y += self.v_y    
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            for block in hits:
                if self.v_y >= 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom
                self.v_y = 0
                
            hits = pygame.sprite.spritecollide(self, self.bubbles, True)
            for h in hits:
                if h.rect.y == h.start_y:
                    self.isinbubble = 1
                    self.image = image_bubble2.convert()
                    self.image.set_colorkey(BLACK)
                    break
            
        else: # monster in a bubble
            self.t += 1
            if self.rect.y < 45:
                self.stop_y()
                if self.rect.x <= 60:
                    self.direction = 1
                elif self.rect.x >= SCREEN_WIDTH - 100:
                    self.direction = -1
                if self.direction == -1:
                    self.left()
                else:
                    self.right()
                if self.t >= 700:
                    self.t = 0
                    self.isinbubble = 0
                    if self.direction == 1:
                        self.image = image_monster_r.convert()
                    else:
                        self.image = image_monster_l.convert()
                    self.image.set_colorkey(BLACK)
            else:
                self.stop_x()
                self.up()
            self.rect.y += self.v_y
            self.rect.x += self.v_x

    def gravity(self):
        if self.v_y == 0:
            self.v_y = 0.8
        else:
            self.v_y += 0.2
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = 0
            self.v_y = 0

    def left(self):
        self.v_x = -2
   
    def right(self):
        self.v_x = 2  
        
    def stop_x(self):
        self.v_x = 0
        
    def stop_y(self):
        self.v_y = 0
    
    def up(self):
        self.v_y = -4





class Bubble(pygame.sprite.Sprite):
    
    def __init__(self, x, y, d):
        super().__init__()
        self.image = image_bubble.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_x = 0
        self.v_y = 0
        self.direction = d
        self.start_x = x
        self.start_y = y
        self.walls = None
        
    def update(self):  
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()
        elif abs(self.rect.x-self.start_x) > 300:
            self.start_x = math.inf
            if self.rect.y < 30:
                self.stop_y()
                if self.rect.x <= 40:
                    self.direction = 1
                elif self.rect.x >= SCREEN_WIDTH - 95:
                    self.direction = -1
                if self.direction == -1:
                    self.left()
                else:
                    self.right()
            else:
                self.stop_x()
                self.up()
            self.rect.x += self.v_x
            self.rect.y += self.v_y
        else:
            if self.direction == -1:
                self.left()
            else:
                self.right()       
            self.rect.x += self.v_x
      
    def left(self):
        self.v_x = -3
   
    def right(self):
        self.v_x = 3  
        
    def stop_x(self):
        self.v_x = 0
        
    def stop_y(self):
        self.v_y = 0
    
    def up(self):
        self.v_y = -3





class Life():
    
    def __init__(self):
        self.image = image_life.convert()
        self.image.set_colorkey(BLACK)
        self.ile = 0
        
    def update(self, screen, font, player):
        self.ile = player.life
        output = "{0}".format(self.ile)
        screen.blit(font.render(output, True, YELLOW), [90,40]) 
        
    
    
    
    
class Score():
    
    def __init__(self):
        self.score = 0
        
    def update(self, screen, font, player):
        self.score = player.score
        output = "{0}".format(self.score)
        screen.blit(font.render(output, True, YELLOW), [845,60])
        screen.blit(font.render('SCORE', True, YELLOW), [845,30])
        
  



class Fruit(pygame.sprite.Sprite):
    
    def __init__(self, x, y, walls):
        super().__init__()
        a = random.randrange(0, 6)
        self.image = image_gems[a].convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_x = random.uniform(-5,5)
        self.v_y = 0
        self.walls = walls
    
    def update(self):  
        
        self.gravity()
        
        self.rect.x += self.v_x
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        for block in hits:
            if self.v_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
                
        self.rect.y += self.v_y
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        if len(hits) > 0:
            self.v_x = 0
        for block in hits:
            self.rect.bottom = block.rect.top 
            self.v_y = 0            

    def gravity(self):
        if self.v_y == 0:
            self.v_y = 1
        else:
            self.v_y += 0.3           
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = 0
            self.v_y = 0

 
    
    
    
class Level():

    def __init__(self, player):
        self.background = None
        self.walls = pygame.sprite.Group()
        self.walls_side = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.player = player
        self.position = None

    def update(self):
        self.walls.update()
        self.walls_side.update()
        self.monsters.update()
        self.bubbles.update()
        self.fruits.update()
 
    def draw(self, screen):
        screen.blit(self.background, [0,0])
        self.walls.draw(screen)
        self.walls_side.draw(screen)
        self.monsters.draw(screen)
        self.bubbles.draw(screen)
        self.fruits.draw(screen)
 




class Level_01(Level):
    
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = image_bg[0].convert()
        self.position = (40, 500)
        tile = image_tile[0].convert()
        
        walls = []
        walls_side = []
        for i in range(0, 561, 40):
            walls_side.append((0, i, tile))
            walls_side.append((960, i, tile))
        for i in range(40, 361, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile))
        for i in range(600, 921, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile)) 
        for i in range(40, 121, 40):
            walls.append((i, 440, tile))
        for i in range(240, 321, 40):
            walls.append((i, 440, tile))            
        for i in range(640, 721, 40):
            walls.append((i, 440, tile))        
        for i in range(840, 921, 40):
            walls.append((i, 440, tile))
        for i in range(120, 281, 40):
            walls.append((i, 320, tile))           
        for i in range(680, 841, 40):
            walls.append((i, 320, tile))
        for i in range(40, 161, 40):
            walls.append((i, 160, tile))     
        for i in range(800, 921, 40):
            walls.append((i, 160, tile))    
        for i in range(320, 641, 40):
            walls.append((i, 200, tile))   
        for i in range(440, 521, 40):
            walls.append((i, 360, tile))               
        
        for w in walls:
            self.walls.add(Wall(w[0], w[1], w[2]))
        for w in walls_side:
            self.walls_side.add(Wall(w[0], w[1], w[2]))

        monsters = [ (40, 110), (920, 110) ]
        for m in monsters:
            mm = Monster(m[0], m[1])
            for w in self.walls:
                mm.walls.add(w)
            for w in self.walls_side:
                mm.walls.add(w)
            self.monsters.add(mm)
            
            
            
   

class Level_02(Level):
    
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = image_bg[1].convert()
        self.position = (480, 460)
        tile = image_tile[1].convert()
        
        walls = []
        walls_side = []
        for i in range(0, 561, 40):
            walls_side.append((0, i, tile))
            walls_side.append((960, i, tile))
        for i in range(40, 161, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile))            
        for i in range(800, 921, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile))
        for i in range(280, 681, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile))
            walls.append((i, 520, tile))
        for i in range(120, 801, 40):
            walls.append((i, 400, tile))
        for i in range(320, 641, 40):
            walls.append((i, 280, tile))
            walls.append((i, 120, tile))
        for i in range(200, 241, 40):
            walls.append((i, 200, tile))
        for i in range(720, 761, 40):
            walls.append((i, 200, tile))      
        walls.append((280, 240, tile))
        walls.append((680, 240, tile))
        walls.append((280, 160, tile))
        walls.append((680, 160, tile))
        
        for w in walls:
            self.walls.add(Wall(w[0], w[1], w[2]))
        for w in walls_side:
            self.walls_side.add(Wall(w[0], w[1], w[2]))

        monsters = [ (400, 200), (500, 320), (200, 80), (800, 80) ]
        for m in monsters:
            mm = Monster(m[0], m[1])
            for w in self.walls:
                mm.walls.add(w)
            for w in self.walls_side:
                mm.walls.add(w)
            self.monsters.add(mm)     
        
              
        
        
        
class Level_03(Level):
    
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = image_bg[2].convert()
        self.position = (900, 500)
        tile = image_tile[2].convert()
        
        walls = []
        walls_side = []
        for i in range(0, 561, 40):
            walls_side.append((0, i, tile))
            walls_side.append((960, i, tile))
        for i in range(40, 961, 40):
            walls_side.append((i, 0, tile))
            walls.append((i, 560, tile))            
        walls.append((40, 440, tile))
        walls.append((80, 440, tile))
        walls.append((120, 400, tile))
        walls.append((120, 360, tile))
        walls.append((80, 320, tile))
        walls.append((40, 320, tile))
        walls.append((120, 160, tile))
        walls.append((120, 200, tile))
        walls.append((160, 240, tile))
        walls.append((200, 240, tile))
        walls.append((240, 200, tile))
        walls.append((240, 160, tile))
        for i in range(400, 761, 40):
            walls.append((i, 160, tile)) 
        for i in range(480, 961, 40):
            walls.append((i, 320, tile))     
                   
        for w in walls:
            self.walls.add(Wall(w[0], w[1], w[2]))
        for w in walls_side:
            self.walls_side.add(Wall(w[0], w[1], w[2]))

        monsters = [ (50, 380), (170, 180), (920, 260), (820, 260), (700, 70), (600, 70), (200, 500) ]
        for m in monsters:
            mm = Monster(m[0], m[1])
            for w in self.walls:
                mm.walls.add(w)
            for w in self.walls_side:
                mm.walls.add(w)
            self.monsters.add(mm)     
                
        
        
        
        
        

