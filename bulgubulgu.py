import pygame
import definitions
from definitions import *


def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode([definitions.SCREEN_WIDTH, definitions.SCREEN_HEIGHT])
    pygame.display.set_caption("Bulgubulgu")
    pygame.mouse.set_visible(False)
    
    font = pygame.font.SysFont(".kenpixel_blocks.ttf", 45, True, False)
    font2 = pygame.font.SysFont(".kenpixel_blocks.ttf", 80, True, False)
    
    settings_file = open("settings.txt", "r")
    settings = list(map(int, settings_file.readlines()))
    settings_file.close()
    
    background_music = 'backmusic.wav'
    pygame.mixer.music.load(background_music)    
    if settings[0] == 1:
        pygame.mixer.music.play(-1)
  

    all_players = pygame.sprite.Group()
  
    player = Player()
    all_players.add(player)
    
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))

    current_level_number = 0
    current_level = level_list[current_level_number]
    
    player.level = current_level
    player.walls = current_level.walls
    player.monsters = current_level.monsters
    player.fruits = current_level.fruits
    player.rect.x = current_level.position[0]
    player.rect.y = current_level.position[1]
        
    life = Life()
    score = Score()
          
    clock = pygame.time.Clock()
    
    time = 0
    
    menu_background = pygame.image.load("tlo_menu.jpg").convert()
    
    window = 1  
    
    while window != 4:
        
        while window == 1:
            screen.blit(menu_background, [0,0])
            t = [ font2.render("BULGUBULGU", False, definitions.YELLOW),
                font.render("START", False, definitions.WHITE),
                font.render("INSTRUCTIONS", False, definitions.WHITE),
                font.render("SETTINGS", False, definitions.WHITE),
                font.render("ENTER", False, definitions.WHITE),
                font.render("I", False, definitions.WHITE),
                font.render("S", False, definitions.WHITE) ]
            r = [None for i in range(7)]
            for i in range(7):
                r[i] = t[i].get_rect()            
            r[0].center = screen.get_width()/2, 100
            r[1].center = screen.get_width()/2-200, 250
            r[2].center = screen.get_width()/2-200, 350
            r[3].center = screen.get_width()/2-200, 450
            r[4].center = screen.get_width()/2+200, 250
            r[5].center = screen.get_width()/2+200, 350
            r[6].center = screen.get_width()/2+200, 450
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    window = 4
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    window = 2
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    window = 3    
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    pygame.quit()
            for i in range(7):
                screen.blit(t[i], r[i])
            pygame.draw.rect(screen, definitions.WHITE, [r[4].center[0]-80,r[4].center[1]-30,160,60],5)
            pygame.draw.rect(screen, definitions.WHITE, [r[5].center[0]-30,r[5].center[1]-30,60,60],5)
            pygame.draw.rect(screen, definitions.WHITE, [r[6].center[0]-30,r[6].center[1]-30,60,60],5)
            pygame.display.flip()
    
        while window == 2:
            screen.blit(menu_background, [0,0])
            t = [ font.render("CONTROLS", False, definitions.YELLOW),
                font.render("LEFT", False, definitions.WHITE),
                font.render("RIGHT", False, definitions.WHITE),
                font.render("UP", False, definitions.WHITE),
                font.render("SPACE", False, definitions.WHITE),
                font.render("move left", False, definitions.WHITE),
                font.render("move right", False, definitions.WHITE),
                font.render("jump", False, definitions.WHITE),
                font.render("shoot", False, definitions.WHITE),
                font.render("Press ENTER to start or BACKSPACE to go back.", False, definitions.YELLOW) ]
            r = [None for i in range(10)]
            for i in range(10):
                r[i] = t[i].get_rect()            
            r[0].center = screen.get_width()/2, 50
            r[1].center = screen.get_width()/2-200, 150
            r[2].center = screen.get_width()/2-200, 250
            r[3].center = screen.get_width()/2-200, 350
            r[4].center = screen.get_width()/2-200, 450
            r[5].center = screen.get_width()/2+200, 150
            r[6].center = screen.get_width()/2+200, 250
            r[7].center = screen.get_width()/2+200, 350
            r[8].center = screen.get_width()/2+200, 450
            r[9].center = screen.get_width()/2, 550
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    window = 4
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    window = 1
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    pygame.quit()
            for i in range(10):
                screen.blit(t[i], r[i])
            pygame.display.flip()
        
        while window == 3:
            screen.blit(menu_background, [0,0])
            t = [ font.render("SETTINGS", False, definitions.YELLOW),
                font.render("SOUND", False, definitions.WHITE),
                font.render("ON", False, definitions.WHITE),
                font.render("Press SPACE to turn sound off.", False, definitions.WHITE), 
                font.render("Press ENTER to start or BACKSPACE to go back.", False, definitions.YELLOW) ]
            file = open("settings.txt", 'r').readlines()
            if file[0] == '0':
                t[3] = font.render("Press SPACE to turn sound on.", False, definitions.WHITE)   
                t[2] = font.render("OFF", False, definitions.WHITE)
            r = [None for i in range(5)]
            for i in range(5):
                r[i] = t[i].get_rect()            
            r[0].center = screen.get_width()/2, 100
            r[1].center = screen.get_width()/2-200, 250
            r[2].center = screen.get_width()/2+200, 250
            r[3].center = screen.get_width()/2, 400
            r[4].center = screen.get_width()/2, 550
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    file = open("settings.txt", 'r').readlines()
                    if file[0] == '1':
                        file[0] = '0'
                        pygame.mixer.music.stop()
                        t[2] = font.render("OFF", False, definitions.WHITE)
                    else:
                        file[0] = '1'
                        pygame.mixer.music.play()
                        t[2] = font.render("ON", False, definitions.WHITE)
                    file2 = open("settings.txt", 'w')
                    file2.writelines(file)
                    file2.close()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    window = 4
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    window = 1    
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    pygame.quit()
            for i in range(5):
                screen.blit(t[i], r[i])
            pygame.display.flip()
    
    while window == 4:
        screen.blit(menu_background, [0,0])
        t = [ font2.render("LEVEL 1", False, definitions.YELLOW),
              font.render("PRESS ENTER TO START", False, definitions.WHITE) ]
        r = [None for i in range(2)]
        for i in range(2):
            r[i] = t[i].get_rect()            
        r[0].center = screen.get_width()/2, 200
        r[1].center = screen.get_width()/2, 400            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                window = 5
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.display.quit()
                pygame.quit()
        for i in range(2):
                screen.blit(t[i], r[i])
        pygame.display.flip()
    

    the_end = False
    while not the_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                the_end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left()
                if event.key == pygame.K_RIGHT:
                    player.right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    b = player.shoot()
                    current_level.bubbles.add(b)
                    for m in current_level.monsters:
                        m.bubbles.add(b)
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and player.v_x != 0:
                    player.stop()
    
        all_players.update()
        current_level.update()
                
        if len(current_level.monsters) == 0:
            time += 1
            if time >= 200:
                next_level = False
                if current_level_number < len(level_list)-1:
                    current_level_number += 1
                    while not next_level:
                        screen.blit(menu_background, [0,0])
                        t = [ font2.render("LEVEL %d"%(current_level_number+1), False, definitions.YELLOW),
                              font.render("PRESS ENTER TO START", False, definitions.WHITE) ]
                        r = [None for i in range(2)]
                        for i in range(2):
                            r[i] = t[i].get_rect()            
                        r[0].center = screen.get_width()/2, 200
                        r[1].center = screen.get_width()/2, 400
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                next_level = True
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.display.quit()
                                pygame.quit()
                        for i in range(2):
                            screen.blit(t[i], r[i])
                        pygame.display.flip()
                    current_level = level_list[current_level_number]
                    player.level = current_level
                    player.fruits = current_level.fruits
                    player.rect.x, player.rect.y = current_level.position
                    player.v_x, player.v_y = 0, 0 #
                else:  
                    while not next_level:
                        screen.blit(menu_background, [0,0])
                        t = [ font2.render("CONGRATULATIONS,", False, definitions.YELLOW),
                              font2.render("Y O U   W O N !  :)", False, definitions.YELLOW),
                              font.render("PRESS ENTER TO PLAY AGAIN", False, definitions.WHITE) ]
                        r = [None for i in range(3)]
                        for i in range(3):
                            r[i] = t[i].get_rect()            
                        r[0].center = screen.get_width()/2, 200
                        r[1].center = screen.get_width()/2, 280
                        r[2].center = screen.get_width()/2, 400
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                main()
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.display.quit()
                                pygame.quit()
                        for i in range(3):
                            screen.blit(t[i], r[i])
                        pygame.display.flip()
                    the_end = True
                time = 0       
                        
                
    
        if not the_end:
            current_level.draw(screen)
            player.walls = current_level.walls
            player.walls_side = current_level.walls_side
            player.monsters = current_level.monsters
            current_level.fruits = player.fruits 
            player.bubbles = current_level.bubbles
            if player.protected == True:
                player.protected_time += 1
            if player.protected_time >= 200:
                player.protected_time = 0
                player.protected = False
                if player.direction == 1:
                    player.image = image_player_r.convert()
                else:
                    player.image = image_player_l.convert()
                player.image.set_colorkey(BLACK)
                       
            life.update(screen, font, player)
            screen.blit(life.image, [30,30])
            pygame.draw.rect(screen, definitions.YELLOW, [20,20,100,62], 4)
            score.update(screen, font, player)
            pygame.draw.rect(screen, definitions.YELLOW, [828,20,152,75], 4)                     
            all_players.draw(screen) 
            
            if player.life <= 0:
                while True:
                    t = [ font2.render("GAME OVER! :(", False, definitions.YELLOW),
                          font.render("PRESS ENTER TO PLAY AGAIN", False, definitions.WHITE) ]
                    r = [None for i in range(2)]
                    for i in range(2):
                        r[i] = t[i].get_rect()            
                    r[0].center = screen.get_width()/2, 200
                    r[1].center = screen.get_width()/2, 400
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            main()
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pygame.display.quit()
                            pygame.quit()
                    for i in range(2):
                        screen.blit(t[i], r[i])
                    pygame.display.flip()
            
                                          
            clock.tick(60)
            pygame.display.flip()
      
    pygame.quit()
                    
if __name__ == "__main__":
    main()
                   
 