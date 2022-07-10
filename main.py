from tkinter import font
import pygame
import sys
import random
from player import Player
import words
from pygame.locals import *


class Wordle:
    
    def __init__(self):
        self.words = words
        self.sys = sys
        self.width = 633 
        self.height = 900
        self.backgroundColor = (50,50,50)
        self.textColor = (255,255,255)


    '''
    Functions
    '''

    def draw_screen(self,caption):  
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        screen.fill(self.backgroundColor)
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)
        return screen
            
    #draws button - does not handle collision
    def draw_button(self,x,y,width,height,screen,button_color,text,font,text_color,outline=0):
        button = pygame.Rect(x,y,width,height)
        pygame.draw.rect(screen,(button_color), button,outline)
        self.draw_text(text,font,text_color,screen,x+10,y+10)
        return button

    def draw_text(self,text,font,color,surface,x,y):
        textobj = font.render(text,1,color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj,textrect)

    def draw_inputBox(self,x,y,width,height,screen,inputBox_color,text,font,text_color,outline=2):
        textobj = font.render(text,1,text_color)
        width = max(100,textobj.get_width()+10)
        inputBox = pygame.Rect(x,y,width,height)
        pygame.draw.rect(screen,(inputBox_color), inputBox,outline)
        textrect = textobj.get_rect()
        textrect.topleft = (x+5,y+5)
        screen.blit(textobj,textrect)
        return inputBox
            

    ''' 
    Screens
    '''


    def start_screen(self):
    
        screen = self.draw_screen('Wordle')
         
        running = True
        while running:

            font = pygame.font.SysFont(None,30)
            mx,my = pygame.mouse.get_pos()
            
            screen.fill(self.backgroundColor)
            self.draw_text('Wordle',font,self.textColor,screen,250,40)
            
            login_button = self.draw_button(250,100,100,50,screen,(255,0,0),'Login',font,self.textColor)
            register_button = self.draw_button(250,300,100,50,screen,(255,0,0),'Register',font,self.textColor)
            
            #Button 1 collision 
            if login_button.collidepoint((mx,my)):
                if click:
                    self.login_screen(screen)
            if register_button.collidepoint((mx,my)):
                if click:
                    self.registor_screen(screen)

            #Events
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                
            
            pygame.display.update()
            mainClock.tick(60)
                

    def login_screen(self,screen):
        username = ''
        password = ''
        click1 = False
        click2 = False
        running = True
        while running:

            header_font = pygame.font.SysFont(None,50)
            text_font = pygame.font.SysFont(None,30)
            input_font = pygame.font.SysFont(None,20)
            mx,my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Login',header_font,self.textColor,screen,20,20)
            
            
            self.draw_text("Username:",text_font, self.textColor,screen,250,300)
            name_box = self.draw_inputBox(250,330,100,25,screen,(255,255,255),username,input_font,self.textColor,2)

            self.draw_text("Password:",text_font, self.textColor,screen,250,600)
            password_box = self.draw_inputBox(250,630,100,25,screen,(255,255,255),password,input_font,self.textColor,2)

            back_button = self.draw_button(250,800,100,50,screen,(255,0,0),'Back',text_font,self.textColor)
            
            #Events
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.exit_screen()             
                
                if event.type == MOUSEBUTTONDOWN:
                    if name_box.collidepoint(event.pos):
                        click1 = True
                    else:
                        click1 = False
                    if password_box.collidepoint(event.pos):
                        click2 = True
                    else:
                        click2 = False
                    if back_button.collidepoint((mx,my)): 
                        running = False

                if event.type == pygame.KEYDOWN:
                    if click1 == True:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    if click2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode
                        
           


            pygame.display.update()
            mainClock.tick(60)

    def registor_screen(self,screen):
        running = True
        while running:

            font = pygame.font.SysFont(None,50)
            mx,my = pygame.mouse.get_pos()

            screen.fill((0,0,0))
            self.draw_text('Register',font,(255,255,255),screen,20,20)
            
            
            back_button = self.draw_button(250,800,100,50,screen,(255,0,0),'Back',font,(255,255,255))
        
            #Button 1 collision 
            
            if back_button.collidepoint((mx,my)):
                if click:
                    running = False
            
            #Events
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()
            mainClock.tick(60)
    
    def exit_screen(self):
        pygame.quit()
        sys.exit()

'''
Main
'''

def main():
    W = Wordle()
    pygame.init()
    
    global mainClock
    mainClock = pygame.time.Clock()

    W.start_screen()

if __name__ == "__main__":
    main()