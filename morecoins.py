from turtle import pos
import pygame
import money
import visuals
import button
import random
import sys

pygame.init()

# Colors
TEXT_COL = (1, 231, 3)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fonts
font_money = pygame.font.SysFont("coolvetica", 35)
font_lose = pygame.font.SysFont("coolvetica", 60)



# Background Colors
BACKGROUND_COLOR = (15, 33, 47)
BACKGROUNDSHADOW_COLOR = (25, 44, 56)
MONEY_SHADOW_COLOR = (33, 55, 67)

# Rectangles
top_rectangle_shadow = (0, 0, 1280, 90)
left_rectangle_shadow = (0, 0, 200, 720)


# Variables
radius = 10

def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def draw_rounded_vortex_rect(surface, color, rect, radius):
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius - 1, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius - 1), radius)
    pygame.draw.circle(surface, color, (rect.right - radius - 1, rect.bottom - radius - 1), radius)
    pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
    pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))


def morecoins():

    # Background and Top Rectangles
    visuals.screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)
    
    money_logo = button.Button(990, 20, visuals.money_logo_img)
    clicked = False

    pos_x1, pos_y1 = random.randint(230, 900), random.randint(100, 580)
    velocity_x1 = 3
    velocity_y1 = -3
   
    pos_x2, pos_y2 = random.randint(230, 900), random.randint(100, 580)
    velocity_x2 = -3
    velocity_y2 = 3
    
    pos_x3, pos_y3 = random.randint(230, 900), random.randint(100, 580)
    velocity_x3 = 3
    velocity_y3 = 3
    
    pos_x5, pos_y5 = random.randint(230, 900), random.randint(100, 580)
    velocity_x5 = -3
    velocity_y5 = -3
    
    pos_x4, pos_y4 = random.randint(230, 900), random.randint(100, 580)
    velocity_x4 = 3
    velocity_y4 = 3
    
    game_rect = pygame.Rect(200, 90, 1040, 590)
    


    clock = pygame.time.Clock()

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
                

        visuals.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
        pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)

        money_logo.draw(visuals.screen)
        draw_text('MORE COINS', font_lose, WHITE, 550, 25, visuals.screen)
                
        

                
        pos_x3 += velocity_x3
        pos_y3 += velocity_y3

        pos_x1 += velocity_x1
        pos_y1 += velocity_y1
        
        pos_x2 += velocity_x2
        pos_y2 += velocity_y2
        
        pos_x5 += velocity_x5
        pos_y5 += velocity_y5
        
        pos_x4 += velocity_x4
        pos_y4 += velocity_y4
        
        if pos_x1 < game_rect.left or pos_x1 > game_rect.right:
            velocity_x1 = -velocity_x1
        if pos_y1 < game_rect.top or pos_y1 > game_rect.bottom:
            velocity_y1 = -velocity_y1  
            
        if pos_x2 < game_rect.left or pos_x2 > game_rect.right:
            velocity_x2 = -velocity_x2
        if pos_y2 < game_rect.top or pos_y2 > game_rect.bottom:
            velocity_y2 = -velocity_y2

        if pos_x3 < game_rect.left or pos_x3 > game_rect.right:
            velocity_x3 = -velocity_x3
        if pos_y3 < game_rect.top or pos_y3 > game_rect.bottom:
            velocity_y3 = -velocity_y3
            
        if pos_x4 < game_rect.left or pos_x4 > game_rect.right:
            velocity_x4 = -velocity_x4
        if pos_y4 < game_rect.top or pos_y4 > game_rect.bottom:
            velocity_y4 = -velocity_y4
            
        if pos_x5 < game_rect.left or pos_x5 > game_rect.right:
            velocity_x5 = -velocity_x5
        if pos_y5 < game_rect.top or pos_y5 > game_rect.bottom:
            velocity_y5 = -velocity_y5
        
        coin1 = button.Button(pos_x1, pos_y1, visuals.hundred_chip_img)
        coin2 = button.Button(pos_x2, pos_y2, visuals.five_chip_img)
        coin3 = button.Button(pos_x3, pos_y3, visuals.fifty_chip_img)
        coin4 = button.Button(pos_x4, pos_y4, visuals.twentyfive_chip_img)
        coin5 = button.Button(pos_x5, pos_y5, visuals.ten_chip_img)
        
        
        
        coin1.draw(visuals.screen)
        coin2.draw(visuals.screen)      
        coin3.draw(visuals.screen)
        coin4.draw(visuals.screen)      
        coin5.draw(visuals.screen)
        
        if clicked and coin1.square.collidepoint(pygame.mouse.get_pos()):
            clicked = False
            money.money += random.randint(1, 6)
           
        if clicked and coin2.square.collidepoint(pygame.mouse.get_pos()):
            clicked = False
            money.money += random.randint(1, 6)      
        
        if clicked and coin3.square.collidepoint(pygame.mouse.get_pos()):
            clicked = False
            money.money += random.randint(1, 6)
                
        if clicked and coin4.square.collidepoint(pygame.mouse.get_pos()):
            clicked = False
            money.money += random.randint(1, 6)        
                
        if clicked and coin5.square.collidepoint(pygame.mouse.get_pos()):
            clicked = False
            money.money += random.randint(1, 6)        
                
                
              
        

        
            

        
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(money.money_rectangle), radius)
       

        draw_text(f"${money.money}", font_money, money.MONEY_TEXT_COLOR, 1063, 33, visuals.screen)


      
        pygame.display.flip()
        clock.tick(60)
