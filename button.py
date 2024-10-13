import pygame


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.square = self.image.get_rect()
        self.square.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        action = False
        pos= pygame.mouse.get_pos()
        
        if self.square.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, (self.square.x, self.square.y))
        
        return action
    






