
import pygame
import random
import sys
import copy
import button
import visuals
import money
import time
from coin_finder import play_coin_finder

pygame.init()

# Colors
TEXT_COL = (1, 231, 3)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
font_money = pygame.font.SysFont("coolvetica", 35)
font_lose = pygame.font.SysFont("coolvetica", 60)

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


# Variables
radius = 10
cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'jack', 'queen', 'king', 'ace']
symbols = ['clubs', 'diamonds', 'spades', 'hearts']
one_deck = [card + '_' + symbol for card in cards for symbol in symbols]
number_of_decks = 5
gamedeck = copy.deepcopy(number_of_decks * one_deck)

def draw_rounded_vortex_rect(surface, color, rect, radius):
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius - 1, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius - 1), radius)
    pygame.draw.circle(surface, color, (rect.right - radius - 1, rect.bottom - radius - 1), radius)
    pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
    pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))

def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def ran_card(deck):
    return random.choice(deck)

def calculate_aces(cards):
    value = 0
    aces = 0
    
    for card in cards:
        card_val = card_value(card)
        value += card_val
        if card_val == 11:
            aces += 1
    
    # Ajustar el valor del As si el total es mayor a 21
    while value > 21 and aces > 0:
        value -= 10  # Convertir un As de 11 a 1
        aces -= 1
    
    return value

def move_and_draw_card(card_x, card_y, target_x, target_y, move_speed, card_image, visuals):
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
    if distance > 0:
        pygame.draw.rect(visuals.screen, BACKGROUND_COLOR, (card_x - dx / distance * move_speed, card_y - dy / distance * move_speed, 135, 196))
    visuals.screen.blit(card_image, (card_x, card_y))

    return card_x, card_y

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

def card_value(card):
    card_value_str = card.split('_')[0] 
    
    if card_value_str.isdigit():
        return int(card_value_str)  
    elif card_value_str in ['jack', 'queen', 'king']:
        return 10 
    elif card_value_str == 'ace':
        return 11  
    return 0  

def verify_cards_hit(player_cards):
    player = player_cards
    hit = False

    if player <= 21:
        hit = True

    return hit
   
def new_game2(wait_lose, rect_win, bet_amount, play_again_button):
    if wait_lose == 480:
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_win, 10)
        draw_text('YOU HAVE LOST!', font_lose, WHITE, 701, 269, visuals.screen)
        draw_text(f'-${bet_amount}', font_lose, RED, 815, 340, visuals.screen)
        if play_again_button.draw(visuals.screen):
            play_blackjack()

def new_game4(wait_lose, rect_win, bet_amount, play_again_button, money_sumed, money_closed):
    if wait_lose == 480:
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_win, 10)
        draw_text("IT'S A TIE", font_lose, WHITE, 701, 269, visuals.screen)
        draw_text(f'+${bet_amount}', font_lose, TEXT_COL, 815, 340, visuals.screen)
        if not money_sumed:
            money.money = money_closed + bet_amount
            money_sumed = True
        if play_again_button.draw(visuals.screen):
            play_blackjack()

def new_game3(wait_lose, rect_win, bet_amount, play_again_button, money_sumed, money_closed):
    if wait_lose == 480:
        
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_win, 10)
        draw_text('YOU HAVE WON!', font_lose, WHITE, 701, 269, visuals.screen)
        draw_text(f'+${bet_amount}', font_lose, TEXT_COL, 815, 340, visuals.screen)
        if not money_sumed:
            money.money = money_closed + bet_amount * 2
            money_sumed = True
        if play_again_button.draw(visuals.screen):
            play_blackjack()

def play_blackjack():
    visuals.screen.fill(BACKGROUND_COLOR)
   
    # Instance buttons
    hit_disabled_button = button.Button(259, 170, visuals.hit_disabled_img)
    stand_disabled_button = button.Button(259, 270, visuals.stand_disabled_img)
    double_disabled_button = button.Button(259, 370, visuals.double_disabled_img)
    hit_enabled_button = button.Button(259, 170, visuals.hit_enabled_img)
    stand_enabled_button = button.Button(259, 270, visuals.stand_enabled_img)
    double_enabled_button = button.Button(259, 370, visuals.double_enabled_img)
    bet_button = button.Button(259, 470, visuals.bet_img)
    clear_bet_button = button.Button(413, 645, visuals.clear_bet_img)
    five_chip_button = button.Button(254, 570, visuals.five_chip_img)
    ten_chip_button = button.Button(304, 570, visuals.ten_chip_img)
    twentyfive_chip_button = button.Button(354, 570, visuals.twentyfive_chip_img)
    fifty_chip_button = button.Button(404, 570, visuals.fifty_chip_img)
    hundred_chip_button = button.Button(454, 570, visuals.hundred_chip_img)
    play_again_button = button.Button(740, 405, visuals.play_again_img)

    card_x0, card_y0 = 1060, 145
    card_x1, card_y1 = 1060, 145
    card_x2, card_y2 = 1060, 145
    card_x3, card_y3 = 1060, 145
    card_x4, card_y4 = 1060, 145
    card_x5, card_y5 = 1060, 145
    card_x6, card_y6 = 1060, 145
    card_x7, card_y7 = 1060, 145
    card_x8, card_y8 = 1060, 145
    card_x9, card_y9 = 1060, 145
    card_x10, card_y10 = 1060, 145
    card_x11, card_y11 = 1060, 145
    card_x12, card_y12 = 1060, 145
      
    money_sumed = False
    
    target_x, target_y = 690, 130
    move_speed = 9
  
    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)



    draw_text('BLACKJACK', font_lose, WHITE, 550, 25, visuals.screen)

    money_logo = button.Button(990, 20, visuals.money_logo_img)
    money_logo.draw(visuals.screen)

    rect = pygame.Rect(actions_rect)
    rect2 = pygame.Rect(250, 150, 240, 300)
    rect_number_dealer = pygame.Rect(587, 310, 65, 41)
    rect_number_player = pygame.Rect(587, 459, 65, 41)
    rect_win = pygame.Rect(rect_end)
    

    draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect, radius)
    
    rect_clearbet = pygame.Rect(bet_rect)
    rect_numberbet = pygame.Rect(bet_number_rect)
    rect_double = pygame.Rect(0, 0, 300, 300)
    
    bet_button.draw(visuals.screen)

    bet_amount = 0
    bet_closed = False
    bet_doubled = False
    bet_wait = True
    money_closed = 0
    hit_pressed = False
    hit_2, hit_3, hit_4, hit_5 = False, False, False, False
    

    can_hit = True
    dealer_pick1 = False
    dealer_pick2 = False
    dealer_pick3 = False

    stand_pressed = False
    double_pressed = False
    not_doubled = True
    
    five_chip_button.draw(visuals.screen)
    ten_chip_button.draw(visuals.screen)
    twentyfive_chip_button.draw(visuals.screen)
    fifty_chip_button.draw(visuals.screen)
    hundred_chip_button.draw(visuals.screen)
    
    cards = []
    
    sum_dealer_card = 0
    sum_player_card = 0

    dealer_cards = []
    player_cards = []
    wait_lose, wait_win = 1, 1
    wait_lose1, wait_win1 = 1, 1
    wait_lose2, wait_win2 = 1, 1
    wait_lose3, wait_win3 = 1, 1
    wait_lose4, wait_win4 = 1, 1
    wait_lose5, wait_win5 = 1, 1
    wait_lose6, wait_win6 = 1, 1
    wait_lose10, wait_win10 = 1, 1
    wait_lose11, wait_win11 = 1, 1
    wait_lose12, wait_win12 = 1, 1
      

    dealer_cards_xy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        clock.tick(60)
        if  not bet_closed:
            pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect2)
            hit_disabled_button.draw(visuals.screen)
            stand_disabled_button.draw(visuals.screen)
            double_disabled_button.draw(visuals.screen)
        
        visuals.screen.blit(visuals.backcard['back_card'], (card_x9, card_y9))
        #avatars
        visuals.screen.blit(visuals.dealer_avatar_img, (555, 160))
        visuals.screen.blit(visuals.player_avatar_img, (555, 520))
        
        

        
        # Update bet amount and money
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
        if bet_button.draw(visuals.screen) and bet_amount > 0:
            bet_closed = True
            random.shuffle(gamedeck)
            money_closed = money.money
            # REDRAW TEXT AND BUTTONS AFTER BET
            
            draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect_clearbet, radius)
            draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_numberbet, radius)
            draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 300, 655, visuals.screen)
            
        
            
        if bet_closed:            
            #suffle cards
            ran_card(gamedeck)
            cards += [ran_card(gamedeck)]
            
#-----------------------------------------------------------------------------------------------------------------------------------------------            
            #first card dealer
            card_x0, card_y0 = move_and_draw_card(card_x0, card_y0, 735, 110, move_speed, visuals.backcard['back_card'], visuals)
            dealer_cards_xy[0] = card_x0

            if dealer_cards_xy[0] == 735:
                visuals.screen.blit(visuals.images[cards[0]], (card_x0, card_y0))
                dealer_cards = [cards[0]]
                sum_dealer_card = calculate_aces(dealer_cards)
                
                #write sum dealer
                draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                

                #second card player                  
                card_x1, card_y1 = move_and_draw_card(card_x1, card_y1, 735, 500, move_speed, visuals.backcard['back_card'], visuals)
                dealer_cards_xy[1] = card_x1

                if dealer_cards_xy[1] == 735:
                   visuals.screen.blit(visuals.images[cards[1]], (card_x1, card_y1))
                   player_cards = [(cards[1])]
                   sum_player_card = calculate_aces(player_cards) 
                   
                   #write sum player
                   draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                   draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)

                   #third card backcard 
                   card_x2, card_y2 = move_and_draw_card(card_x2, card_y2, 765, 135, move_speed, visuals.backcard['back_card1'], visuals)
                   dealer_cards_xy[2] = card_x2

                   if dealer_cards_xy[2] == 765:
                       #backcard, don't sum instant, check later
                       visuals.screen.blit(visuals.backcard['back_card1'], (card_x2, card_y2))
                       
                       
                       #forth card
                       card_x3, card_y3 = move_and_draw_card(card_x3, card_y3, 765, 475, move_speed, visuals.backcard['back_card'], visuals)
                       dealer_cards_xy[3] = card_x3
                       
                       if dealer_cards_xy[3] == 765:
                           visuals.screen.blit(visuals.images[cards[3]], (card_x3, card_y3))
                           player_cards = [cards[1], cards[3]]
                           sum_player_card = calculate_aces(player_cards)

                           #write sum dealer
                           draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                           draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)

                           bet_wait = False
                           pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect2)
            
                           if (hit_pressed or hit_enabled_button.draw(visuals.screen)) and can_hit:
                               hit_pressed = True
                               
                               double_disabled_button.draw(visuals.screen)
                               visuals.screen.blit(visuals.hit_enabled_img, (259, 170))#test and corrected
                               visuals.screen.blit(visuals.stand_enabled_img, (259, 270))
                               #new_card
                               card_x4, card_y4 = move_and_draw_card(card_x4, card_y4, 795, 450, move_speed, visuals.backcard['back_card1'], visuals)
                               dealer_cards_xy[4] = card_x4
                               if dealer_cards_xy[4] == 795:
                                    visuals.screen.blit(visuals.images[cards[4]], (card_x4, card_y4))
                                    player_cards = [cards[1], cards[3], cards[4]]
                                    sum_player_card = calculate_aces(player_cards)
                                    
                                    #write text card
                                    draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                                    draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)
                                    
                                    #verify if win or lose 
                                    alive = verify_cards_hit(sum_player_card)
                                    
                                    if not alive:
                                        wait_lose, wait_win = move_and_draw_time(wait_lose, wait_win, 480, 1, 6, visuals.pixel_img, visuals)
                                        new_game2(wait_lose, rect_win, bet_amount, play_again_button)
                                            
                                    elif hit_2 or hit_enabled_button.draw(visuals.screen):
                                        hit_2 = True
                                        card_x5, card_y5 = move_and_draw_card(card_x5, card_y5, 825, 430, move_speed, visuals.backcard['back_card1'], visuals)
                                        dealer_cards_xy[5] = card_x5
                                        
                                        if dealer_cards_xy[5] == 825:
                                            visuals.screen.blit(visuals.images[cards[5]], (card_x5, card_y5))
                                            player_cards = [cards[1], cards[3], cards[4], cards[5]]
                                            sum_player_card = calculate_aces(player_cards)
                                    
                                            #write text card
                                            draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                                            draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)
                                    
                                            #verify if win or lose 
                                            alive = verify_cards_hit(sum_player_card)
                                            if not alive:
                                                wait_lose10, wait_win10 = move_and_draw_time(wait_lose10, wait_win10, 480, 1, 6, visuals.pixel_img, visuals)
                                                new_game2(wait_lose10, rect_win, bet_amount, play_again_button)
                                            elif hit_3 or hit_enabled_button.draw(visuals.screen):
                                                hit_3 = True
                                                card_x6, card_y6 = move_and_draw_card(card_x6, card_y6, 855, 410, move_speed, visuals.backcard['back_card1'], visuals)
                                                dealer_cards_xy[6] = card_x6
                                        
                                                if dealer_cards_xy[6] == 855:
                                                    visuals.screen.blit(visuals.images[cards[6]], (card_x6, card_y6))
                                                    player_cards = [cards[1], cards[3], cards[4], cards[5], cards[6]]
                                                    sum_player_card = calculate_aces(player_cards)
                                    
                                                    #write text card
                                                    draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                                                    draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)
                                    
                                                    #verify if win or lose 
                                                    alive = verify_cards_hit(sum_player_card)
                                                    if not alive:
                                                        wait_lose11, wait_win11 = move_and_draw_time(wait_lose11, wait_win11, 480, 1, 6, visuals.pixel_img, visuals)
                                                        new_game2(wait_lose11, rect_win, bet_amount, play_again_button)
                                                    
                                                    elif hit_4 or hit_enabled_button(visuals.screen):
                                                        hit_4 = True
                                                        card_x7, card_y7 = move_and_draw_card(card_x7, card_y7, 885, 390, move_speed, visuals.backcard['back_card1'], visuals)
                                                        dealer_cards_xy[7] = card_x7
                                        
                                                        if dealer_cards_xy[7] == 885:
                                                            visuals.screen.blit(visuals.images[cards[7]], (card_x7, card_y7))
                                                            player_cards = [cards[1], cards[3], cards[4], cards[5], cards[6], cards[7]]
                                                            sum_player_card = calculate_aces(player_cards)
                                    
                                                            #write text card
                                                            draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                                                            draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 765, 135, visuals.screen)
                                    
                                                            #verify if win or lose 
                                                            alive = verify_cards_hit(sum_player_card)
                                                            if not alive:
                                                                wait_lose12, wait_win12 = move_and_draw_time(wait_lose12, wait_win12, 480, 1, 6, visuals.pixel_img, visuals)
                                                                new_game2(wait_lose12, rect_win, bet_amount, play_again_button) 
                                                                
                           elif double_pressed or double_enabled_button.draw(visuals.screen):                    
                               not_doubled = False

                               if bet_amount <= money.money and not hit_pressed and not bet_doubled and bet_closed and not bet_wait: 
                                   double_pressed = True
                                   money.money -= bet_amount
                                   bet_amount *= 2
                                   bet_doubled = True
                                   can_hit = False
                                   draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 300, 655, visuals.screen)
                               if double_pressed:
                                   visuals.screen.blit(visuals.hit_disabled_img, (259, 170))#test and corrected
                                   visuals.screen.blit(visuals.stand_disabled_img, (259, 270))
                                   visuals.screen.blit(visuals.double_disabled_img, (259, 370))
                                   
                               #card doubled
                               card_x8, card_y8 = move_and_draw_card(card_x8, card_y8, 795, 450, move_speed, visuals.backcard['back_card1'], visuals)
                               dealer_cards_xy[8] = card_x8
                               ################
                               if dealer_cards_xy[8] == 795:
                                    visuals.screen.blit(visuals.images[cards[8]], (card_x8, card_y8))
                                    player_cards = [cards[1], cards[3], cards[8]]
                                    sum_player_card = calculate_aces(player_cards)
                                    
                                    #write text card
                                    draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_player, 8)
                                    draw_text(f"{sum_player_card}", font_money, money.MONEY_TEXT_COLOR, 607, 467, visuals.screen)
                                    
                                    #verify if win or lose 
                                    alive = verify_cards_hit(sum_player_card)
                                    
                                    if not alive:
                                        wait_lose, wait_win = move_and_draw_time(wait_lose, wait_win, 480, 1, 6, visuals.pixel_img, visuals)
                                        if wait_lose == 480:    
                                            new_game2(wait_lose, rect_win, bet_amount, play_again_button)
                                    else:
                                        wait_lose, wait_win = move_and_draw_time(wait_lose, wait_win, 480, 1, 6, visuals.pixel_img, visuals)
                                        
                                        #reveal dealers card
                                        if wait_lose == 480 and sum_player_card <= 21:    
                                            visuals.screen.blit(visuals.images[cards[9]], (card_x2, card_y2))
                                            dealer_cards = [cards[0], cards[9]]
                                            sum_dealer_card = calculate_aces(dealer_cards)
                                            draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 6)
                                            draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                            
                                            #####hereeeeeeeeeeeeeee
                                            if dealer_pick1 or sum_dealer_card < 17:
                                                wait_lose4, wait_win4 = move_and_draw_time(wait_lose4, wait_win4, 480, 1, 6, visuals.pixel_img, visuals)
                                                if wait_lose4 == 480:
                                                
                                                    dealer_pick1 = True
                                                    card_x10, card_y10 = move_and_draw_card(card_x10, card_y10, 795, 155, 6, visuals.backcard['back_card'], visuals)
                                                    dealer_cards_xy[10] = card_x10

                                                    if dealer_cards_xy[10] == 795:
                                                        visuals.screen.blit(visuals.images[cards[10]], (card_x10, card_y10))
                                                        dealer_cards = [(cards[0]), (cards[9]), (cards[10])]
                                                        sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                        #write sum dealer
                                                        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                        draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                    
                                                    
                                                        if sum_dealer_card > 16:
                                                            #win or lose
                                                            if sum_dealer_card == sum_player_card:
                                                            
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game4(wait_lose1, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                            elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game3(wait_lose1, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                            elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game2(wait_lose1, rect_win, bet_amount, play_again_button)
                                                        else:
                                                            if dealer_pick2 or sum_dealer_card < 17:
                                                                dealer_pick2 = True
                                                            
                                                                card_x11, card_y11 = move_and_draw_card(card_x11, card_y11, 825, 185, 6, visuals.backcard['back_card'], visuals)
                                                                dealer_cards_xy[11] = card_x11

                                                                if dealer_cards_xy[11] == 825:
                                                                    visuals.screen.blit(visuals.images[cards[11]], (card_x11, card_y11))
                                                                    dealer_cards = [(cards[0]), (cards[9]), (cards[10]), (cards[11])]
                                                                    sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                                    #write sum dealer
                                                                    draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                                    draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                                    #win or lose
                                                                    if sum_dealer_card == sum_player_card:
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 8, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game4(wait_lose2, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                                    elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 6, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game3(wait_lose2, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                                    elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 6, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game2(wait_lose2, rect_win, bet_amount, play_again_button)
                                                                    else:
                                                                        if dealer_pick3 or sum_dealer_card < 17:
                                                                            dealer_pick3 = True
                                                            
                                                                            card_x12, card_y12 = move_and_draw_card(card_x12, card_y12, 855, 205, 6, visuals.backcard['back_card'], visuals)
                                                                            dealer_cards_xy[12] = card_x12

                                                                            if dealer_cards_xy[12] == 855:
                                                                                visuals.screen.blit(visuals.images[cards[12]], (card_x12, card_y12))
                                                                                dealer_cards = [(cards[0]), (cards[9]), (cards[10]), (cards[11]), (cards[12])]
                                                                                sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                                                    #write sum dealer
                                                                                draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                                                draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                                                #win or lose
                                                                                if sum_dealer_card == sum_player_card:
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 8, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game4(wait_lose5, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                                                elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 6, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game3(wait_lose5, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                                                elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 6, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game2(wait_lose5, rect_win, bet_amount, play_again_button)
                                                        
                                                        
                                            elif ((sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21) and not dealer_pick1 and not dealer_pick2:
                                                            
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game3(wait_lose3, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                      
                                                     
                                            elif (sum_player_card == sum_dealer_card) and not dealer_pick1 and not dealer_pick2:   
                                                            
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game4(wait_lose3, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                            else:
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game2(wait_lose3, rect_win, bet_amount, play_again_button)
                                                
                                                            
                                        
                           if not_doubled and (stand_pressed or stand_enabled_button.draw(visuals.screen)):
                               stand_pressed = True
                               
                               pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect2)
                               hit_disabled_button.draw(visuals.screen)
                               stand_disabled_button.draw(visuals.screen)
                               double_disabled_button.draw(visuals.screen)
                               
                               wait_lose, wait_win = move_and_draw_time(wait_lose, wait_win, 480, 1, 6, visuals.pixel_img, visuals)
                                        
                                        #reveal dealers card
                               if wait_lose == 480:    
                                            visuals.screen.blit(visuals.images[cards[9]], (card_x2, card_y2))
                                            dealer_cards = [cards[0], cards[9]]
                                            sum_dealer_card = calculate_aces(dealer_cards)
                                            draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 6)
                                            draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                            
                                            if dealer_pick1 or sum_dealer_card < 17:
                                                wait_lose4, wait_win4 = move_and_draw_time(wait_lose4, wait_win4, 480, 1, 6, visuals.pixel_img, visuals)
                                                if wait_lose4 == 480:
                                                
                                                    dealer_pick1 = True
                                                    card_x10, card_y10 = move_and_draw_card(card_x10, card_y10, 795, 155, 6, visuals.backcard['back_card'], visuals)
                                                    dealer_cards_xy[10] = card_x10

                                                    if dealer_cards_xy[10] == 795:
                                                        visuals.screen.blit(visuals.images[cards[10]], (card_x10, card_y10))
                                                        dealer_cards = [(cards[0]), (cards[9]), (cards[10])]
                                                        sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                        #write sum dealer
                                                        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                        draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                    
                                                    
                                                        if sum_dealer_card > 16:
                                                            #win or lose
                                                            if sum_dealer_card == sum_player_card:
                                                            
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game4(wait_lose1, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                            elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game3(wait_lose1, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                            elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                wait_lose1, wait_win1 = move_and_draw_time(wait_lose1, wait_win1, 480, 1, 6, visuals.pixel_img, visuals)
                                                                if wait_lose1 == 480:
                                                                    new_game2(wait_lose1, rect_win, bet_amount, play_again_button)
                                                        else:
                                                            if dealer_pick2 or sum_dealer_card < 17:
                                                                dealer_pick2 = True
                                                            
                                                                card_x11, card_y11 = move_and_draw_card(card_x11, card_y11, 825, 185, 6, visuals.backcard['back_card'], visuals)
                                                                dealer_cards_xy[11] = card_x11

                                                                if dealer_cards_xy[11] == 825:
                                                                    visuals.screen.blit(visuals.images[cards[11]], (card_x11, card_y11))
                                                                    dealer_cards = [(cards[0]), (cards[9]), (cards[10]), (cards[11])]
                                                                    sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                                    #write sum dealer
                                                                    draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                                    draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                                    #win or lose
                                                                    if sum_dealer_card == sum_player_card:
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 8, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game4(wait_lose2, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                                    elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 6, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game3(wait_lose2, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                                    elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                        wait_lose2, wait_win2 = move_and_draw_time(wait_lose2, wait_win2, 480, 1, 6, visuals.pixel_img, visuals)
                                                                        if wait_lose2 == 480:
                                                                            new_game2(wait_lose2, rect_win, bet_amount, play_again_button)
                                                                    else:
                                                                        if dealer_pick3 or sum_dealer_card < 17:
                                                                            dealer_pick3 = True
                                                            
                                                                            card_x12, card_y12 = move_and_draw_card(card_x12, card_y12, 855, 205, 6, visuals.backcard['back_card'], visuals)
                                                                            dealer_cards_xy[12] = card_x12

                                                                            if dealer_cards_xy[12] == 855:
                                                                                visuals.screen.blit(visuals.images[cards[12]], (card_x12, card_y12))
                                                                                dealer_cards = [(cards[0]), (cards[9]), (cards[10]), (cards[11]), (cards[12])]
                                                                                sum_dealer_card = calculate_aces(dealer_cards) 
                                                    
                                                                                    #write sum dealer
                                                                                draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_number_dealer, 8)
                                                                                draw_text(f"{sum_dealer_card}", font_money, money.MONEY_TEXT_COLOR, 607, 319, visuals.screen)
                                                    
                                                                                #win or lose
                                                                                if sum_dealer_card == sum_player_card:
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 8, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game4(wait_lose5, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                                        
                                                        
                                                                                elif (sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21:
                                                        
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 6, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game3(wait_lose5, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                       
                                                     
                                                                                elif (sum_player_card < sum_dealer_card and sum_dealer_card >= 17):   
                                                        
                                                                                    wait_lose5, wait_win5 = move_and_draw_time(wait_lose5, wait_win5, 480, 1, 6, visuals.pixel_img, visuals)
                                                                                    if wait_lose5 == 480:
                                                                                        new_game2(wait_lose5, rect_win, bet_amount, play_again_button)
                                                        
                                                        
                                            elif ((sum_player_card > sum_dealer_card and sum_dealer_card >= 17) or sum_dealer_card > 21) and not dealer_pick1 and not dealer_pick2:
                                                            
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game3(wait_lose3, rect_win, bet_amount, play_again_button, money_sumed, money_closed)                                                      
                                                     
                                            elif (sum_player_card == sum_dealer_card) and not dealer_pick1 and not dealer_pick2:   
                                                            
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game4(wait_lose3, rect_win, bet_amount, play_again_button, money_sumed, money_closed)
                                            else:
                                                            wait_lose3, wait_win3 = move_and_draw_time(wait_lose3, wait_win3, 480, 1, 6, visuals.pixel_img, visuals)
                                                            if wait_lose3 == 480:
                                                                new_game2(wait_lose3, rect_win, bet_amount, play_again_button)
                                                

                               
                                    
                           
    
        
        five_chip_button.draw(visuals.screen)
        ten_chip_button.draw(visuals.screen)
        twentyfive_chip_button.draw(visuals.screen)
        fifty_chip_button.draw(visuals.screen)
        hundred_chip_button.draw(visuals.screen)
        
        # Redraw rectangles bet and money
        
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, money.money_rectangle, radius)
        draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, rect_clearbet, radius)
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, rect_numberbet, radius)


        # Clear bet button
        clear_bet_button.draw(visuals.screen)
        bet_button.draw(visuals.screen)
        # Money and bet numbers
        draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 300, 655, visuals.screen)
        draw_text(f"${money.money}", font_money, money.MONEY_TEXT_COLOR, 1063, 33, visuals.screen)
        

        pygame.display.flip()
        