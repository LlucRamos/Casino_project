import pygame
import money
import visuals
import button
import random
import sys
import math

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
actions_rect = (688, 476, 500, 210)
bet_rect = (280, 627, 189, 72)
bet_number_rect = (920, 600, 110, 43)
rect_end = (650, 225, 450, 310)
rect_win = pygame.Rect(rect_end)
rect_roulette = (240, 310, 380, 380)
replay_rect = (220, 120, 330, 140)

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

def create_colored_surface(width, height, color):
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface
    
def create_transparent_surface(width, height, color_with_alpha):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color_with_alpha)
    return surface

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

def rotate_center(surface, image, topleft, angle):
        
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
        surface.blit(rotated_image, new_rect.topleft)
        
def calculate_number(roulette_angle, ball_angle, roulette_numbers):
    total_slots = len(roulette_numbers)
    
    ball_relative_angle = (360 - roulette_angle - ball_angle + 360 - 90) % 360

    slot_angle = 360 / total_slots
    
 
    #landing_index = 37 - int((ball_relative_angle + slot_angle / 2) // slot_angle) % total_slots
    landing_index = (total_slots - int((ball_relative_angle + slot_angle / 2) // slot_angle)) % total_slots
    '''print(f"ball_relative_angle: {ball_relative_angle}")
    print(f"slot_angle: {slot_angle}")
    print(f"landing_index: {landing_index}")'''
    return roulette_numbers[landing_index]

def play_roulette():
    #VARIABLES AND LISTS    
    one_grid = []
    doubleh_grid = []
    doublev_grid = []
    four_grid = []
    zero_one_grid = []
    zero_three_grid = []
    thirdsh_grid = []
    thirdsv_grid = []
    fiftys_grid = []
    
    one_number = 1

    bet_amount = 0
    selected_chip = None
    chip_amount = None
    bet_closed = False
    
    #ROULETTE, POSITIONS AND ANGLES TO ROTATE
    roulette_pos = [240, 310]
    roulette_ang = random.uniform(0, 360)
    roulette_spd = 5  
    numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]  
    round_win = 0

    #BALL POSITION AND PATH TO ROTATE
    
    ball_ang = random.uniform(0, 360)  
    ball_spd = -10  
    ball_path = 135 
    ball_x = 430 + ball_path * math.cos(math.radians(ball_ang))
    ball_y = 500 + ball_path * math.sin(math.radians(ball_ang))
    

   #BACKGROUND AND TOP RECTANGLES 
    visuals.screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, left_rectangle_shadow)
    pygame.draw.rect(visuals.screen, BACKGROUNDSHADOW_COLOR, top_rectangle_shadow)
    draw_rounded_vortex_rect(visuals.screen, BACKGROUNDSHADOW_COLOR, pygame.Rect(actions_rect), radius)
    
    #INSTANCE BUTTONS
    bet_button = button.Button(890, 500, visuals.bet_img)   
    clear_bet_button = button.Button(1040, 600, visuals.clear_bet_img)
    five_chip_button = button.Button(720, 523, visuals.five_chip_img)
    ten_chip_button = button.Button(720, 593, visuals.ten_chip_img)
    twentyfive_chip_button = button.Button(783, 491, visuals.twentyfive_chip_img)
    fifty_chip_button = button.Button(783, 558, visuals.fifty_chip_img)
    hundred_chip_button = button.Button(783, 626, visuals.hundred_chip_img)
    visuals.play_again_img = pygame.transform.smoothscale(visuals.play_again_img, (235, 60))
    play_again_button = button.Button(270, 180, visuals.play_again_img)
    
    
    bet_button.draw(visuals.screen)
    
    clear_bet_button.draw(visuals.screen)

    #testing positions
    betting_board = button.Button(580, 130, visuals.betting_board_img)
    roulette = button.Button(240, 310, visuals.roulette_img)
    ball = button.Button(ball_x, ball_y, visuals.ball_img)
    
    betting_board.draw(visuals.screen)
    roulette.draw(visuals.screen)
    ball.draw(visuals.screen)

    #GRIDS
    one_surface = create_transparent_surface(27, 52, (255, 255, 255, 0))
    two_surface = create_transparent_surface(18, 52, (0, 0, 255, 0))
    two_surface1 = create_transparent_surface(27, 21, (0, 0, 255, 0))
    four_surface = create_transparent_surface(18, 23, (255, 0, 0, 0))
    visuals.zero_img.set_alpha(0)
    thirdsh_surface = create_transparent_surface(168, 40, (255, 255, 255, 0))
    thirdsv_surface = create_transparent_surface(34, 62, (255, 255, 255, 0))
    fiftys_surface = create_transparent_surface(75, 40, (255, 255, 255, 0))
    
    
    #1 NUMBER BET GRID
    for row in range(3):
        for column in range(12):
            x = 672 + column * 45.35
            y = 138 + row * 75
            one = button.Button(x, y, one_surface)
            
            one.draw(visuals.screen)
            one_grid.append(one)
            if row == 0:
                one_number = 3 + column * 3  
            if row == 1:
                 one_number = 2 + column * 3
            if row == 2:
                 one_number = 1 + column * 3   
            one.onenumber = one_number
            one.bet_amount = 0

    #2 NUMBERS BET GRID
    for row in range(3):
        for column in range(12):
            x = 653 + column * 45.35
            y = 138 + row * 75
            twoh = button.Button(x, y, two_surface)
            twoh.draw(visuals.screen)
            doubleh_grid.append(twoh)
            if row == 0:
                first_num = 3 + 3 * column
                second_num = first_num - 3
            if row == 1:
                first_num = 2 + 3 * column
                second_num = max(0, first_num - 3)
            if row == 2:
                first_num = 1 + 3 * column
                second_num = max(0, first_num - 3)
            
            twoh.numbers = (second_num, first_num)
            twoh.bet_amount = 0

    for row in range(2):
        for column in range(12):
            x = 672 + column * 45.35
            y = 191 + row * 75
            twov = button.Button(x, y, two_surface1)
            twov.draw(visuals.screen)
            doublev_grid.append(twov)
            if row == 0:
                first_num = 3 + 3 * column
                second_num = first_num - 1
            if row == 1:
                first_num = 2 + 3 * column
                second_num = first_num - 1
            
            
            twov.numbers = (second_num, first_num)
            twov.bet_amount = 0
    
    #4 NUMBERS BET GRID
    for row in range(2):
        for column in range(11):
            x = 699 + column * 45.35
            y = 190 + row * 75
            four = button.Button(x, y, four_surface)
            four.draw(visuals.screen)
            four_grid.append(four)
            if row == 0:
                first_num = 3 + column * 3 
                second_num = first_num - 1
                third_num = first_num + 3
                four_num = second_num + 3             
            if row == 1:
                first_num = 2 + column * 3 
                second_num = first_num - 1
                third_num = first_num + 3
                four_num = second_num + 3

            four.numbers = (first_num, second_num, third_num, four_num)
            four.bet_amount = 0
            
    #GRIDS FOR 0
    #0 ONE
    for row in range(1):
        for column in range(1):
            x = 586 + column * 45.35
            y = 138 + row * 75
            zero = button.Button(x, y, visuals.zero_img)
            zero.draw(visuals.screen)
            zero_one_grid.append(zero)
            first_num = 0
            zero.numbers = (first_num, first_num)
            zero.bet_amount = 0

    for row in range(2):
        for column in range(1):
            x = 656 + column * 45.35
            y = 190 + row * 75
            zero_three = button.Button(x, y, four_surface)
            zero_three.draw(visuals.screen)
            zero_three_grid.append(zero_three)
            if row == 0:
                first_num = 0 
                second_num = 3
                third_num = 2
                        
            if row == 1:
                first_num = 0 
                second_num = 2
                third_num = 1
                

            zero_three.numbers = (first_num, second_num, third_num)
            zero_three.bet_amount = 0
    #GRIDS FOR THIRDS AND 50'S       
     
    for row in range(1):
        for column in range(3):
            x = 671 + column * 180
            y = 353 + row * 75
            thirdsh = button.Button(x, y, thirdsh_surface)
            thirdsh.draw(visuals.screen)
            thirdsh_grid.append(thirdsh)
            if column == 0:
                twelves = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                        
            if column == 1:
                twelves = (13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24)
              
            if column == 2:
                twelves = (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36)
            
            thirdsh.numbers = twelves
            thirdsh.bet_amount = 0
       
     

            
    for row in range(3):
        for column in range(1):
            x = 1210 + column * 180
            y = 137 + row * 72
            thirdsv = button.Button(x, y, thirdsv_surface)
            thirdsv.draw(visuals.screen)
            thirdsv_grid.append(thirdsv)
            if row == 0:
                twelves = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                        
            if row == 1:
                twelves = (13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24)
              
            if row == 2:
                twelves = (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36)
            
            thirdsv.numbers = twelves
            thirdsv.bet_amount = 0
            
    for row in range(1):
        for column in range(6):
            x = 673 + column * 89.5
            y = 403 + row * 75
            fiftys = button.Button(x, y, fiftys_surface)
            fiftys.draw(visuals.screen)
            fiftys_grid.append(fiftys)
            mid = ()
            even = ()
            colors = ()
            if column == 0:
                mid = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
                        
            if column == 1:
                even = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36)
              
            if column == 2:
                colors = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
                #28
            if column == 3:
                colors = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
                        
            if column == 4:
                even = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35)
              
            if column == 5:
                mid = (19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36)
    
            fiftys.numbers1 = mid
            fiftys.numbers2 = even
            fiftys.numbers3 = colors
            fiftys.bet_amount = 0
      
    clock = pygame.time.Clock()
    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        #code updating       

        if five_chip_button.draw(visuals.screen):
            selected_chip = five_chip_button
            chip_amount = 5
        if ten_chip_button.draw(visuals.screen):
            selected_chip = ten_chip_button
            chip_amount = 10
            
        if twentyfive_chip_button.draw(visuals.screen):
            selected_chip = twentyfive_chip_button
            chip_amount = 25
            
        if fifty_chip_button.draw(visuals.screen):
            selected_chip = fifty_chip_button
            chip_amount = 50

        if hundred_chip_button.draw(visuals.screen):
            selected_chip = hundred_chip_button
            chip_amount = 100
            
        
        if bet_button.draw(visuals.screen) and bet_amount > 0:
            bet_closed = True

        if clear_bet_button.draw(visuals.screen) and not bet_closed:
            money.money += bet_amount
            play_roulette()
            
        
            
        if not bet_closed:
            #GRIDS 
            for grid_button in one_grid:
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 7, y + 4))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount

                
                
            for grid_button in doubleh_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 13, y + 4))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                    
                    
                
            for grid_button in doublev_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 7, y - 13))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                    
                
            for grid_button in four_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 13, y - 12))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                    
                
                
            for grid_button in zero_one_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x + 14, y + 80))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                    
        
            for grid_button in zero_three_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 13, y - 12))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                    print(grid_button.numbers)
        
            for grid_button in thirdsh_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x + 60, y - 3))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                
                
            for grid_button in thirdsv_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x - 2, y + 7))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                
                
            for grid_button in fiftys_grid:   
                if selected_chip and grid_button.draw(visuals.screen) and money.money >= chip_amount:  
                    x, y = grid_button.square.topleft           
                    visuals.screen.blit(selected_chip.image, (x + 15, y - 1))
                    bet_amount += chip_amount
                    money.money -= chip_amount
                    grid_button.bet_amount += chip_amount
                
        if bet_closed and bet_amount > 0:
            visuals.screen.blit(visuals.roulette_shadow_img, rect_roulette)
            
            roulette_ang = (roulette_ang + roulette_spd) % 360
            ball_ang = (ball_ang - ball_spd) % 360
            ball_x = 430 + ball_path * math.cos(math.radians(ball_ang))
            ball_y = 500 + ball_path * math.sin(math.radians(ball_ang))

            if roulette_spd > 0.2:
                roulette_spd *= random.uniform(0.980, 1) 
            if ball_spd < -0.2:
                ball_spd *= random.uniform(0.980, 1) 

            visuals.screen.blit(visuals.roulette_shadow_img, rect_roulette)


            rotate_center(visuals.screen, visuals.roulette_img, roulette_pos, roulette_ang)
            visuals.screen.blit(visuals.ball_img, (ball_x - visuals.ball_img.get_width() // 2, ball_y - visuals.ball_img.get_height() // 2))

            if roulette_spd <= 0.2 and ball_spd <= 0.2:
                result = calculate_number(roulette_ang, ball_ang, numbers) 
                print(f"The ball landed on number: {result}")
                roulette_spd = 0
                ball_spd = 0

                round_win = 0
                for grid_button in one_grid:
                    if grid_button.onenumber == result:  
                        win = grid_button.bet_amount * 36
                        round_win += win
                        print(round_win)
                

                for grid_button in doubleh_grid:
                    if result in grid_button.numbers:
                        win = grid_button.bet_amount * 18  
                        round_win += win
                        print(round_win)
                        
                for grid_button in doublev_grid:
                    if result in grid_button.numbers:
                        win = grid_button.bet_amount * 18  
                        round_win += win
                        print(round_win)

                for grid_button in four_grid:
                    if result in grid_button.numbers:
                        win = grid_button.bet_amount * 9  
                        round_win += win
                        print(round_win)
                
                for grid_button in zero_one_grid:

                    if hasattr(grid_button, 'numbers') and result == grid_button.numbers:
                        win = grid_button.bet_amount * 36
                        round_win += win


 
                for grid_button in zero_three_grid:

                    if hasattr(grid_button, 'numbers') and result in grid_button.numbers:
                        win = grid_button.bet_amount * 12
                        round_win += win
         
         
                
                for grid_button in thirdsh_grid:
                    if result in grid_button.numbers:
                        win = grid_button.bet_amount * 3  
                        round_win += win
                        print(round_win)
                 
                for grid_button in thirdsv_grid:
                    if result in grid_button.numbers:
                        win = grid_button.bet_amount * 3  
                        round_win += win
                        print(round_win)
                        
                for grid_button in fiftys_grid:
                    if result in grid_button.numbers1:
                        win = grid_button.bet_amount * 2  
                        round_win += win
                        print(round_win)
                    else:
                        win = 0
                        round_win += win
                        print(round_win)
                for grid_button in fiftys_grid:
                    if result in grid_button.numbers2:
                        win = grid_button.bet_amount * 2 
                        round_win += win
                        print(round_win)
                    else:
                        win = 0
                        round_win += win
                        print(round_win)
                        
                for grid_button in fiftys_grid:
                    if result in grid_button.numbers3:
                        win = grid_button.bet_amount * 2 
                        round_win += win
                        print(round_win)
                    else:
                        win = 0
                        round_win += win
                        print(round_win)   


        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(money.money_rectangle), radius)      
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(bet_number_rect), radius)
        draw_rounded_vortex_rect(visuals.screen, MONEY_SHADOW_COLOR, pygame.Rect(replay_rect), radius)        
        draw_text(f"You won: ${round_win}", font_money, money.MONEY_TEXT_COLOR, 300, 145, visuals.screen)
        draw_text(f"${bet_amount}", font_money, money.MONEY_TEXT_COLOR, 930, 610, visuals.screen)
        draw_text(f"${money.money}", font_money, money.MONEY_TEXT_COLOR, 1063, 33, visuals.screen)

        if play_again_button.draw(visuals.screen):
            money.money += round_win
            play_roulette()
            
        
        pygame.display.flip()
        clock.tick(60)
