import pygame
import sys
import button
import visuals
import money
from blackjack_game import play_blackjack, draw_text, draw_rounded_vortex_rect
from coin_finder import play_coin_finder
from roulette_game import play_roulette
from morecoins import morecoins

#* Inicializa Pygame
pygame.init()

# Dimensions    
top_rectangle_shadow = (0, 0, 1280, 90)

radius= 10

pygame.display.set_caption("CASINO")
game_menu = False

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#text color
TEXT_COL = (255, 255, 255)
font = pygame.font.Font('FONTS/RioGrande.ttf', 60)
font_money = pygame.font.SysFont("coolvetica", 35)
text = font.render("PRESS SPACE TO START", True, TEXT_COL)
loading_txt = font.render("LOADING...", True, TEXT_COL)

#text p and v
x = 365
y = 330

v = 0.10  
dir = 1  

#backgrand colors
BACKGROUND_COLOR = (15, 33, 47)
BACKGROUNDSHADOW_COLOR = (25, 44, 56)
MONEY_SHADOW_COLOR = ((33, 55, 67))

#instances buttons
blackjack_button = button.Button(80, 115, visuals.blackjack_img)        
coin_finder_button = button.Button(380, 115, visuals.mines_img)
roulette_button = button.Button(680, 115, visuals.roulette_button_img)          
morecoins_button = button.Button(980, 115, visuals.morecoins_img)

st_pos_X, st_pos_Y = 0, 0
x_chip, y_chip = 0, 0 
v_chip = 0.12            
dir_chip = 1         
last_time = pygame.time.get_ticks()
new_chip_time = 1500
chips = []    
initial_positions = [
    (-40, 50),
    (110, 50),
    (260, 50),
    (410, 50),
    (560, 50),
    (710, 50),
    (860, 50),
    (1010, 50),
    (1160, 50),
    (-40, 200),
    (-40, 350),
    (-40, 500), 
    (-40, 650)
    
]
delays = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def background_chips(chip, current_time):
    
    if current_time >= chip["start_time"]:
     
        chip["x"] += chip["dir"] * chip["v"]
        chip["y"] += chip["dir"] * chip["v"]
        

        if chip["y"] > 720:
            return None  

    return chip["x"], chip["y"]

    
#gameloop
run = True
while run:         
    visuals.screen.blit(visuals.starting_img, (0, 0))
     #draw shadow background
    visuals.screen.fill(BACKGROUND_COLOR)
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= new_chip_time:
            for i, position in enumerate(initial_positions):
                if current_time - last_time >= delays[i] + new_chip_time:
                    chips.append({
                        "image": visuals.chip_img,
                        "x": position[0],
                        "y": position[1],
                        "v": v_chip,  
                        "dir": dir_chip,                       
                        "start_time": last_time + delays[i]  
                    })
            last_time = current_time  
    
    
    #instancw buttons on MENU
    if game_menu == True:       
       
        for chip in chips[:]:  
            result = background_chips(chip, current_time)
            if result is None:
                chips.remove(chip) 
            else:
                chip["x"], chip["y"] = result
                visuals.screen.blit(chip["image"], (chip["x"], chip["y"]))

        

        pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)

        #show money
        money_logo = button.Button(990, 20, visuals.money_logo_img)
        money_logo.draw(visuals.screen)
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, money.money_rectangle, radius)
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, money.money_rectangle, radius)
        draw_text(f"${money.money}", font_money, money.MONEY_TEXT_COLOR, 1063, 33, visuals.screen)
        
        #game's buttons
        if blackjack_button.draw(visuals.screen):
           #BLACKJACK GAME
           play_blackjack()
           
        if coin_finder_button.draw(visuals.screen):
            play_coin_finder()
            
        if roulette_button.draw(visuals.screen):
            play_roulette()
            
        if morecoins_button.draw(visuals.screen):
            morecoins()
    else:
        y += dir * v


        if y <= 320 or y >= 340 :
            dir *= -1

         # Dibuja la pantalla
        visuals.screen.blit(visuals.starting_img, (0, 0))
        visuals.screen.blit(text, (x, y))
        
        
        
        
        
        
        
        
        
        

        
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_menu = True
        if event.type == pygame.QUIT:
            run = False
            
        
    pygame.display.update()
pygame.quit()


