import pygame
import sys
import random
from player import Player
import words



class Wordle:
    
    def __init__(self):
        self.words = words
        self.sys = sys
        self.backgroundColor = (50,50,50)
        self.width = 633 
        self.height = 900
        #self.mx,self.my = pygame.mouse.get_pos()

    '''
    Functions
    '''

    def draw_screen(self,caption):
        
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        screen.fill(self.backgroundColor)
        pygame.display.flip()
        mainClock = pygame.time.Clock()
        pygame.display.update()
        mainClock.tick(60)
        return screen
            
            
    #draws button - does not handle collision
    def draw_button(self,left,top,width,height,screen,color):
        button = pygame.Rect(left,top,width,height)
        pygame.draw.rect(screen,(color), button)
        return button

    def draw_text(self,text,font,color,surface,x,y):
        textobj = font.render(text,1,color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj,textrect)
        
            

    ''' 
    Screens
    '''


    def start_screen(self):
        screen = self.draw_screen('start screen')
        
        
        running = True
        while running:
            
            mx,my = pygame.mouse.get_pos()
            
            button_1 = self.draw_button(100,100,100,200,screen,(255,0,0))
            font = pygame.font.SysFont(None,20)
            self.draw_text('yo',font,(255,255,255),screen,20,20)

            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if button_1.collidepoint((mx,my)):
                    running = False
                


    def login_screen(self):
        pass

    def registor_screen(self):
        pass
    
    def exit_screen(self):
        pygame.quit()



def main():
    W = Wordle()
    pygame.init()
    
    W.start_screen()
    #open()

if __name__ == "__main__":
    main()

