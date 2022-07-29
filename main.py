from tkinter import font
import pygame
import sys
import random
from player import Player
import words
from pygame.locals import *
import json


class Wordle:

    def __init__(self):
        self.words = words
        self.sys = sys
        self.width = 633
        self.height = 900
        self.backgroundColor = (50, 50, 50)
        self.textColor = (255, 255, 255)
        self.DB = "DB.jsons"
        self.Alp = ['Q','W','E','R','T','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

    '''
    Functions
    '''

    def draw_screen(self, caption,width,height):
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        screen.fill(self.backgroundColor)
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)
        return screen

    # draws button - does not handle collision
    def draw_button(self, x, y, width, height, screen, button_color, text, font, text_color, outline=0):
        button = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (button_color), button, outline)
        self.draw_text(text, font, text_color, screen, x+10, y+10)
        return button

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_inputBox(self, x, y, width, height, screen, inputBox_color, text, font, text_color, outline=2):
        textobj = font.render(text, 1, text_color)
        width = max(100, textobj.get_width()+10)
        inputBox = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (inputBox_color), inputBox, outline)
        textrect = textobj.get_rect()
        textrect.topleft = (x+5, y+5)
        screen.blit(textobj, textrect)
        return inputBox

    def draw_keyboard(self,x,y,screen,button_color,text_color,font):
        runs = 0
        dx = x
        lines = 0
        for letter in self.Alp:

            # changes the line line of the keyboard 
            if runs > 8:
                x = dx
                y = y + 25
                lines += 1
                runs = 0
            # ensures the last line of the keyboard is even
            if lines == 2:
                x += 25
                lines = 0 
            
            letter = self.draw_button(x,y,20,20,screen,button_color,letter,font,text_color)
            runs += 1 
            x += 25

        

    def check_login(self, username, password,screen):

        with open("DB.json") as DB:
            data = DB.read()
            self.DB = json.loads(data)
            DB.close()

        if username == '':
            return 'ERROR: you forgot username'
        if password == '':
            return 'ERROR: You forgot passowrd '
        if username and password != '':
            if username in self.DB:
                if password == self.DB[username]['password']:
                    self.wordle_screen(screen)
                    # Start the wordle  
                else:
                    return 'password dont match what we got'
            else:
                return 'That username aint real'

    def check_registor(self, username, password,screen):

        with open("DB.json") as DB:
            data = DB.read()
            self.DB = json.loads(data)
            DB.close()

        if username == '':
            return 'ERROR: you forgot username'
        if password == '':
            return 'ERROR: You forgot password'
        if username and password != '':
            if username not in self.DB:
                self.DB[username] = {"password": password,"numGames": 0, "PercWin": 0, "GuessDist": 0}
                with open("DB.json", 'w') as data:
                    json.dump(self.DB, data)
                    data.close()
                    self.login_screen(screen)
            else:
                return 'Username taken'

    ''' 
    Screens
    '''

    def start_screen(self):

        screen = self.draw_screen('Wordle',self.width,self.height)

        running = True
        while running:

            font = pygame.font.SysFont(None, 30)
            mx, my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Wordle', font, self.textColor, screen, 250, 40)

            login_button = self.draw_button(250, 100, 100, 50, screen, (255, 0, 0), 'Login', font, self.textColor)
            register_button = self.draw_button(250, 300, 100, 50, screen, (255, 0, 0), 'Register', font, self.textColor)

            # Button 1 collision
            if login_button.collidepoint((mx, my)):
                if click:
                    self.login_screen(screen)
            if register_button.collidepoint((mx, my)):
                if click:
                    self.registor_screen(screen)

            # Events
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            mainClock.tick(60)

    def login_screen(self, screen):
        username = ''
        password = ''
        error_message = ''
        click1 = False
        click2 = False
        running = True
        while running:

            header_font = pygame.font.SysFont(None, 50)
            text_font = pygame.font.SysFont(None, 30)
            input_font = pygame.font.SysFont(None, 20)
            mx, my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Login', header_font,self.textColor, screen, 20, 20)

            self.draw_text(error_message,text_font,(255,0,0),screen,200,200)

            self.draw_text("Username:", text_font,self.textColor, screen, 250, 300)
            name_box = self.draw_inputBox(250, 330, 100, 25, screen, (255, 255, 255), username, input_font, self.textColor, 2)

            self.draw_text("Password:", text_font,self.textColor, screen, 250, 400)
            password_box = self.draw_inputBox(250, 430, 100, 25, screen, (255, 255, 255), password, input_font, self.textColor, 2)

            enter_button = self.draw_button(250, 700, 100, 50, screen, (255, 0, 0), 'Enter', text_font, self.textColor)

            back_button = self.draw_button(250, 800, 100, 50, screen, (255, 0, 0), 'Back', text_font, self.textColor)

            # Events
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
                    if back_button.collidepoint((mx, my)):
                        running = False
                    if enter_button.collidepoint((mx, my)):
                        error_message = ''
                        error_message  = self.check_login(username, password,screen)

                if event.type == pygame.KEYDOWN:
                    if click1 == True:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif event.key == pygame.K_RETURN:
                            username = username  
                        else:
                            username += event.unicode
                    if click2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        elif event.key == pygame.K_RETURN:
                            password = password
                        else:
                            password += event.unicode
                    if event.key == pygame.K_RETURN:
                        error_message = ''
                        error_message = self.check_login(username, password,screen)

            pygame.display.update()
            mainClock.tick(60)

    def registor_screen(self, screen):
        username = ''
        password = ''
        error_message = ''
        click1 = False
        click2 = False
        running = True
        while running:

            header_font = pygame.font.SysFont(None, 50)
            text_font = pygame.font.SysFont(None, 30)
            input_font = pygame.font.SysFont(None, 20)
            mx, my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Register', header_font,self.textColor, screen, 20, 20)

            self.draw_text(error_message,text_font,(255,0,0),screen,200,200)

            self.draw_text("Username:", text_font,self.textColor, screen, 250, 300)
            name_box = self.draw_inputBox(250, 330, 100, 25, screen, (255, 255, 255), username, input_font, self.textColor, 2)

            self.draw_text("Password:", text_font,self.textColor, screen, 250, 400)
            password_box = self.draw_inputBox(250, 430, 100, 25, screen, (255, 255, 255), password, input_font, self.textColor, 2)

            enter_button = self.draw_button(250, 700, 100, 50, screen, (255, 0, 0), 'Enter', text_font, self.textColor)

            back_button = self.draw_button(250, 800, 100, 50, screen, (255, 0, 0), 'Back', text_font, self.textColor)

            # Events
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
                    if back_button.collidepoint((mx, my)):
                        running = False
                    if enter_button.collidepoint((mx, my)):
                        error_message = ''
                        error_message = self.check_registor(username, password,screen)

                if event.type == pygame.KEYDOWN:
                    if click1 == True:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif event.key == pygame.K_RETURN:
                            username = username  
                        else:
                            username += event.unicode
                    if click2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        elif event.key == pygame.K_RETURN:
                            password = password
                        else:
                            password += event.unicode
                    if event.key == pygame.K_RETURN:
                        error_message = ''
                        error_message = self.check_registor(username, password,screen)

            pygame.display.update()
            mainClock.tick(60)

    def wordle_screen(self,screen):
        username = ''
        password = ''
        error_message = ''
        click1 = False
        click2 = False
        running = True
        while running:

            header_font = pygame.font.SysFont(None, 50)
            text_font = pygame.font.SysFont(None, 30)
            input_font = pygame.font.SysFont(None, 20)
            mx, my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Wordle', header_font,self.textColor, screen, 20, 20)

            self.draw_text(error_message,text_font,(255,0,0),screen,200,200)

            self.draw_text("Guess", text_font,self.textColor, screen, 250, 300)
            guess_box = self.draw_inputBox(250, 330, 100, 25, screen, (255, 255, 255), username, input_font, self.textColor, 2)

            self.draw_keyboard(200,400,screen, (255,0,0), self.textColor,input_font)

            
            enter_button = self.draw_button(250, 700, 100, 50, screen, (255, 0, 0), 'Enter', text_font, self.textColor)

            back_button = self.draw_button(250, 800, 100, 50, screen, (255, 0, 0), 'Back', text_font, self.textColor)

            # Events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.exit_screen()

                if event.type == MOUSEBUTTONDOWN:
                    if guess_box.collidepoint(event.pos):
                        click1 = True
                    else:
                        click1 = False
                    if back_button.collidepoint((mx, my)):
                        running = False
                    if enter_button.collidepoint((mx, my)):
                        error_message = ''
                        #check guess
                        #error_message  = self.check_login(username, password,screen)

                if event.type == pygame.KEYDOWN:
                    if click1 == True:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif event.key == pygame.K_RETURN:
                            username = username  
                        else:
                            username += event.unicode
                    if click2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        elif event.key == pygame.K_RETURN:
                            password = password
                        else:
                            password += event.unicode
                    if event.key == pygame.K_RETURN:
                        error_message = ''
                        #check guess
                        #error_message = self.check_login(username, password,screen)

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
