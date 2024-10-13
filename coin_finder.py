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
font_bombs = pygame.font.SysFont("coolvetica", 35)
font_bombs1 = pygame.font.SysFont("coolvetica", 45)
font_bombs2 = pygame.font.SysFont("coolvetica", 33)


# Background Colors
BACKGROUND_COLOR = (15, 33, 47)
BACKGROUNDSHADOW_COLOR = (25, 44, 56)
MONEY_SHADOW_COLOR = (33, 55, 67)

# Rectangles
top_rectangle_shadow = (0, 0, 1280, 90)
left_rectangle_shadow = (0, 0, 200, 720)
actions_rect = (245, 135, 261, 500)
bet_rect = (280, 627, 189, 72)
bet_number_rect = (291, 645, 110, 43)
rect_end = (650, 225, 450, 310)
rect_win = pygame.Rect(rect_end)

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

def reset_tiles(button_tiles, tile_content, bombs):
    tiles = 25
    coins = tiles - bombs
    content = ['bomb'] * bombs + ['coin'] * coins
    random.shuffle(content)

    for i, tile in enumerate(button_tiles):
        if i < len(content):
            tile_content[i] = content[i]

def move_and_draw_time(card_x, card_y, target_x, target_y, move_speed, card_image, visuals):
    dx = target_x - card_x
    dy = target_y - card_y
    distance = (dx**2 + dy**2)**0.5

    if distance > move_speed:
        dx_normalized = dx / distance
        dy_normalized = dy / distance
        card_x += dx_normalized * move_speed
        card_y += dy_normalized * move_speed
    else:
        card_x, card_y = target_x, target_y
    visuals.screen.blit(card_image, (card_x, card_y))

    return card_x, card_y

def lose(wait_lose, rect_win, bet_amount, play_again_button):
    if wait_lose == 480:
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_win, 10)
        draw_text('YOU HAVE LOST!', font_lose, WHITE, 701, 269, visuals.screen)
        draw_text(f'-${bet_amount}', font_lose, RED, 815, 340, visuals.screen)
        if play_again_button.draw(visuals.screen):
            play_coin_finder()

def win(wait_lose, rect_win, play_again_button, money_sumed, money_closed, checkout):
    if wait_lose == 480:
        
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_win, 10)
        draw_text('YOU HAVE WON!', font_lose, WHITE, 701, 269, visuals.screen)
        draw_text(f'+${checkout}', font_lose, TEXT_COL, 815, 340, visuals.screen)
        if not money_sumed:
            money_sumed = True
            money.money = money_closed + checkout

        if play_again_button.draw(visuals.screen):
            play_coin_finder()            

def play_coin_finder():
    # Variables and Lists
    bet_closed = False
    bet_amount = 0
    money_closed = 0
    money_sumed = False
    
    button_tiles = []
    tile_content = []
    tile_clicked = []

    enable_checkout = False

    tiles = 25
    bombs = 3
    coins = 25 - bombs 
    multiplier = round((tiles / (tiles - bombs) * 0.99), 2)  
    next_multiplier = round((tiles / (tiles - bombs) * 0.99), 2)
    
    first_coin = True
   
    content = ['bomb'] * bombs + ['coin'] * coins
    random.shuffle(content)

    checkout = 0
    checkout_clicked = False
    
    wait_lose, wait_win = 1, 1
    wait_lose1, wait_win1 = 1, 1
    bombed = False

    # Background and Top Rectangles
    visuals.screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)

    # Instance Buttons
    bet_button = button.Button(259, 475, visuals.bet_img)
    checkout_button = button.Button(259, 380, visuals.checkout_img)
    clear_bet_button = button.Button(413, 645, visuals.clear_bet_img)
    add_bomb_button = button.Button(375, 213, visuals.add_bomb_img)
    subtract_bomb_button = button.Button(425, 213, visuals.subtract_bomb_img)
    five_chip_button = button.Button(254, 570, visuals.five_chip_img)
    ten_chip_button = button.Button(304, 570, visuals.ten_chip_img)
    twentyfive_chip_button = button.Button(354, 570, visuals.twentyfive_chip_img)
    fifty_chip_button = button.Button(404, 570, visuals.fifty_chip_img)
    hundred_chip_button = button.Button(454, 570, visuals.hundred_chip_img)
    play_again_button = button.Button(740, 405, visuals.play_again_img)
    
    money_logo = button.Button(990, 20, visuals.money_logo_img)

    for row in range(5):
        for column in range(5):
            x = 550 + column * 105
            y = 130 + row * 105
            tile = button.Button(x, y, visuals.tile_img)
            button_tiles.append(tile)
            tile_content.append(content.pop())
            tile_clicked.append(False)
    
    clock = pygame.time.Clock()

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Redraw background and other elements every frame
        visuals.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
        pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)

        money_logo.draw(visuals.screen)
        draw_text('MINES', font_lose, WHITE, 550, 25, visuals.screen)

        draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, pygame.Rect(actions_rect), radius)

        if five_chip_button.draw(visuals.screen) and 5 <= money.money and not bet_closed:
            bet_amount += 5
            money.money -= 5
        if ten_chip_button.draw(visuals.screen) and 10 <= money.money and not bet_closed:
            bet_amount += 10
            money.money -= 10
        if twentyfive_chip_button.draw(visuals.screen) and 25 <= money.money and not bet_closed:
            bet_amount += 25
            money.money -= 25
        if fifty_chip_button.draw(visuals.screen) and 50 <= money.money and not bet_closed:
            bet_amount += 50
            money.money -= 50
        if hundred_chip_button.draw(visuals.screen) and 100 <= money.money and not bet_closed:
            bet_amount += 100
            money.money -= 100
        if clear_bet_button.draw(visuals.screen) and bet_amount > 0 and not bet_closed:
            money.money += bet_amount
            bet_amount = 0

        if add_bomb_button.draw(visuals.screen) and (bombs < 20 and bombs > 0) and not bet_closed:
            bombs += 1
            multiplier = round(tiles / (tiles-bombs), 2)
            reset_tiles(button_tiles, tile_content, bombs)
            
            next_multiplier = round((tiles / (tiles - bombs) * 0.99), 2)
        if subtract_bomb_button.draw(visuals.screen) and (bombs <= 20 and bombs > 1) and not bet_closed:
            bombs -= 1
            multiplier = round(tiles / (tiles-bombs), 2)
            reset_tiles(button_tiles, tile_content, bombs)
            
            next_multiplier = round((tiles / (tiles - bombs) * 0.99), 2)
   
        if bet_button.draw(visuals.screen) and bet_amount > 0:
            bet_closed = True
            money_closed = money.money
            draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, pygame.Rect(bet_rect), radius)
            draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 300, 655, visuals.screen)
        
        if bet_closed and enable_checkout:
            checkout = round((bet_amount * multiplier), 2)
            
       

        for index, tile in enumerate(button_tiles):
            
            if not tile_clicked[index]:  
                
                if tile.draw(visuals.screen) and bet_closed:
                    content = tile_content[index]
                    enable_checkout = True                    
                    tile_clicked[index] = True
                    
                    if content == 'coin':
                        if first_coin:
                            multiplier = round((tiles / (tiles - bombs) * 0.99), 2)
                            next_multiplier = round(multiplier * ((tiles - 1) / (tiles - 1 - bombs)) * 0.99, 2)
                            first_coin = False
                            tiles -= 1
                        else:
                            multiplier = round(multiplier * ((tiles / (tiles - bombs)) * 0.99), 2)  
                            next_multiplier = round(multiplier * ((tiles - 1) / (tiles - 1 - bombs)) * 0.99, 2)
                            tiles -= 1
            else:         
                x, y = tile.square.topleft
                content = tile_content[index]

                if content == 'coin':
                    visuals.screen.blit(visuals.coin_img, (x + 5, y + 5))
                    

                if  content == 'bomb':
                    bombed = True
                    visuals.screen.blit(visuals.bomb_img, (x + 5, y + 5))
                    
        if bombed:
            wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
            lose(wait_lose1, rect_win, bet_amount, play_again_button)            
                  
        if checkout_clicked or (not bombed and checkout_button.draw(visuals.screen)):
            checkout_clicked = True

            wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
            win(wait_lose1, rect_win, play_again_button, money_sumed, money_closed, checkout)
      

        # Draw all buttons again to ensure visibility
        add_bomb_button.draw(visuals.screen)
        subtract_bomb_button.draw(visuals.screen)
        five_chip_button.draw(visuals.screen)
        ten_chip_button.draw(visuals.screen)
        twentyfive_chip_button.draw(visuals.screen)
        fifty_chip_button.draw(visuals.screen)
        hundred_chip_button.draw(visuals.screen)
        
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(money.money_rectangle), radius)
        draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, pygame.Rect(bet_rect), radius)
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(bet_number_rect), radius)

        clear_bet_button.draw(visuals.screen)
        bet_button.draw(visuals.screen)

        draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 300, 655, visuals.screen)
        draw_text(f"${money.money}", font_money, money.MONEY_TEXT_COLOR, 1063, 33, visuals.screen)

        draw_text('NUMBER OF BOMBS', font_bombs, WHITE, 257, 165, visuals.screen)
        draw_text(f"{bombs}", font_bombs1, WHITE, 305, 218, visuals.screen)
        draw_text('NEXT MULTIPLIER', font_bombs, WHITE, 265, 295, visuals.screen)
        draw_text(f"x{next_multiplier}", font_bombs1, TEXT_COL, 340, 335, visuals.screen)

        checkout_button.draw(visuals.screen)
        if bombed:
            draw_text('Check Out: $0', font_bombs2, WHITE, 268, 408, visuals.screen)
        else:   
            draw_text(f'Check Out: ${checkout}', font_bombs2, WHITE, 268, 408, visuals.screen)

        
        pygame.display.flip()
        clock.tick(60)