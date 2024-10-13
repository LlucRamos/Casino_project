import os
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

#main menu
blackjack_img = pygame.image.load('BUTTON_IMAGES/blackjack_button.png').convert_alpha()
mines_img = pygame.image.load('BUTTON_IMAGES/mines_button.png').convert_alpha()
roulette_button_img = pygame.image.load('BUTTON_IMAGES/roulette_button.png').convert_alpha()
morecoins_img = pygame.image.load('BUTTON_IMAGES/morecoins_bt.png').convert_alpha()
starting_img = pygame.image.load('BUTTON_IMAGES/starting_img.png').convert_alpha()


#sidemenu img
blackjack_sidemenu_img = pygame.image.load('BUTTON_IMAGES/SIDE_BLACKJACK_BUTTON_IMG.jpg').convert_alpha()
    
#actions menu
hit_disabled_img = pygame.image.load('BUTTON_IMAGES/hit_disabled_img.png').convert_alpha()
hit_enabled_img = pygame.image.load('BUTTON_IMAGES/hit_enabled_img.png').convert_alpha()

stand_disabled_img = pygame.image.load('BUTTON_IMAGES/stand_disabled_img.png').convert_alpha()
stand_enabled_img = pygame.image.load('BUTTON_IMAGES/stand_enabled_img.png').convert_alpha()

double_disabled_img = pygame.image.load('BUTTON_IMAGES/double_disabled_img.png').convert_alpha()
double_enabled_img = pygame.image.load('BUTTON_IMAGES/double_enabled_img.png').convert_alpha()

bet_img = pygame.image.load('BUTTON_IMAGES/bet_img.png').convert_alpha()

play_again_img = pygame.image.load('BUTTON_IMAGES/play_again_img.png').convert_alpha()
pixel_img = pygame.image.load('BUTTON_IMAGES/pixel.png').convert_alpha()


#CHIPS IMG
five_chip_img = pygame.image.load('CHIPS_IMAGES/five_chip.png').convert_alpha()
ten_chip_img = pygame.image.load('CHIPS_IMAGES/ten_chip.png').convert_alpha()
twentyfive_chip_img = pygame.image.load('CHIPS_IMAGES/twentyfive_chip.png').convert_alpha()
fifty_chip_img = pygame.image.load('CHIPS_IMAGES/fifty_chip.png').convert_alpha()
hundred_chip_img = pygame.image.load('CHIPS_IMAGES/hundred_chip.png').convert_alpha()
chip_img = pygame.image.load('CHIPS_IMAGES/chip.png').convert_alpha()


#tiles
tile_img = pygame.image.load('CHIPS_IMAGES/tile.png').convert_alpha()

checkout_img = pygame.image.load('BUTTON_IMAGES/checkout.png').convert_alpha()

#money logo
money_logo_img = pygame.image.load('CHIPS_IMAGES/money_logo.png').convert_alpha()
bomb_img = pygame.image.load('CHIPS_IMAGES/bomb.png').convert_alpha()
coin_img = pygame.image.load('CHIPS_IMAGES/money_logo.png').convert_alpha()

#clear bet button
clear_bet_img = pygame.image.load('CHIPS_IMAGES/clear_bet.png').convert_alpha()
add_bomb_img = pygame.image.load('BUTTON_IMAGES/add_img.png').convert_alpha()
subtract_bomb_img = pygame.image.load('BUTTON_IMAGES/subtract_img.png').convert_alpha()


#AVATARS
dealer_avatar_img = pygame.image.load('AVATARS/dealer_img.png').convert_alpha()
player_avatar_img = pygame.image.load('AVATARS/player_img.png').convert_alpha()

#BETTING ROULETTE
betting_board_img = pygame.image.load('ROULETTE/betting_board.png').convert_alpha()
roulette_img = pygame.image.load('ROULETTE/roulette.png').convert_alpha()
roulette_shadow_img = pygame.image.load('ROULETTE/roulette_shadow.png').convert_alpha()
zero_img = pygame.image.load('ROULETTE/zero.png').convert_alpha()
ball_img = pygame.image.load('ROULETTE/ball.png').convert_alpha()



#cards 
#copy backcards
#DIR
image_dir_cards = 'BACKCARDS_CARP/'

#List
backcard = {}

#Load img
for filename in os.listdir(image_dir_cards):
    if filename.endswith('.png'):  
        #import cards
        image_path = os.path.join(image_dir_cards, filename)
        image_name = os.path.splitext(filename)[0]
        original_image = pygame.image.load(image_path)
        #scalae cards
        scaled_image = pygame.transform.smoothscale(original_image, (135, 196))
        backcard[image_name] = scaled_image

#DIR
image_dir_cards = 'CARDS_IMAGES/'

#List
images = {}

#Load img
for filename in os.listdir(image_dir_cards):
    if filename.endswith('.png'):  
        #import cards
        image_path = os.path.join(image_dir_cards, filename)
        image_name = os.path.splitext(filename)[0]
        original_image = pygame.image.load(image_path)
        #scalae cards
        scaled_image = pygame.transform.smoothscale(original_image, (135, 196))
        images[image_name] = scaled_image


# Set the size for the image buttons actions(hit, stand, double)
ACTION_BUTTON_SIZE = (230, 78 )
CHIP_SIZE = (45, 45)
 
# Scale the image to your needed size
hit_disabled_img = pygame.transform.smoothscale(hit_disabled_img, ACTION_BUTTON_SIZE)
hit_enabled_img = pygame.transform.smoothscale(hit_enabled_img, ACTION_BUTTON_SIZE)

stand_disabled_img = pygame.transform.smoothscale(stand_disabled_img, ACTION_BUTTON_SIZE)
stand_enabled_img = pygame.transform.smoothscale(stand_enabled_img, ACTION_BUTTON_SIZE)

double_disabled_img = pygame.transform.smoothscale(double_disabled_img, ACTION_BUTTON_SIZE)
double_enabled_img = pygame.transform.smoothscale(double_enabled_img, ACTION_BUTTON_SIZE)

bet_img = pygame.transform.smoothscale(bet_img, ACTION_BUTTON_SIZE)
checkout_img = pygame.transform.smoothscale(checkout_img, ACTION_BUTTON_SIZE)


five_chip_img = pygame.transform.smoothscale(five_chip_img, CHIP_SIZE)
ten_chip_img = pygame.transform.smoothscale(ten_chip_img, CHIP_SIZE)
twentyfive_chip_img = pygame.transform.smoothscale(twentyfive_chip_img, CHIP_SIZE)
fifty_chip_img = pygame.transform.smoothscale(fifty_chip_img, CHIP_SIZE)
hundred_chip_img = pygame.transform.smoothscale(hundred_chip_img, CHIP_SIZE)
chip_img = pygame.transform.smoothscale(chip_img, CHIP_SIZE)


money_logo_img = pygame.transform.smoothscale(money_logo_img, (53, 53))

clear_bet_img = pygame.transform.smoothscale(clear_bet_img, (42, 42))

pixel_img = pygame.transform.smoothscale(pixel_img, (1, 1))

dealer_avatar_img = pygame.transform.smoothscale(dealer_avatar_img, (130, 130))
player_avatar_img = pygame.transform.smoothscale(player_avatar_img, (130, 130))

add_bomb_img = pygame.transform.smoothscale(add_bomb_img, (42, 42))
subtract_bomb_img = pygame.transform.smoothscale(subtract_bomb_img, (40, 40))

coin_img = pygame.transform.smoothscale(coin_img, (80, 80))
bomb_img = pygame.transform.smoothscale(bomb_img, (80, 80))

roulette_img = pygame.transform.smoothscale(roulette_img, (380, 380))
roulette_shadow_img = pygame.transform.smoothscale(roulette_img, (380, 380))
ball_img = pygame.transform.smoothscale(ball_img, (25, 25))

blackjack_img = pygame.transform.smoothscale(blackjack_img, (246, 590))
mines_img = pygame.transform.smoothscale(mines_img, (246, 590))
roulette_button_img = pygame.transform.smoothscale(roulette_button_img, (246, 590))
morecoins_img = pygame.transform.smoothscale(morecoins_img, (246, 590))