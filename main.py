from tkinter import font
import pygame
import sys
import random
from player import Player
import words
from pygame.locals import *
import json
import pygame.freetype


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

    def draw_guessBox(self, x, y, width, height, screen, inputBox_color, text, font, text_color, outline=2):
        textobj = font.render(text, 1, text_color)
        inputBox = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (inputBox_color), inputBox, outline)
        textrect = textobj.get_rect()
        textrect.topleft = (x+15, y+10)
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

    def draw_guessRow(self, x, y, width, height, screen, inputBox_color, L1,L2,L3,L4,L5, font, text_color, outline=2):
        box1 = self.draw_guessBox(x, y, width, height, screen, inputBox_color, L1,font, text_color)
        box2 = self.draw_guessBox(x+55, y, width, height, screen, inputBox_color, L2,font, text_color)
        box3 = self.draw_guessBox(x+110, y, width, height, screen, inputBox_color, L3,font, text_color)
        box4 = self.draw_guessBox(x+165, y, width, height, screen, inputBox_color, L4,font, text_color)
        box5 = self.draw_guessBox(x+220, y, width, height, screen, inputBox_color, L5,font, text_color)
        return box1

    def draw_guessTable(self, x, y, width, height, screen, inputBox_color, L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15,L16,L17,L18,L19,L20,L21,L22,L23,L24,L25,L26,L27,L28,L29,L30, font, text_color,line, outline=2):
        guess_box = self.draw_guessRow(x, y, width, height, screen, inputBox_color, L1,L2,L3,L4,L5,font, text_color)
        guess_box2 = self.draw_guessRow(x, y+55, width, height, screen, inputBox_color, L6,L7,L8,L9,L10,font, text_color)
        guess_box3 = self.draw_guessRow(x, y+110, width, height, screen, inputBox_color, L11,L12,L13,L14,L15,font, text_color)
        guess_box4 = self.draw_guessRow(x, y+165, width, height, screen, inputBox_color, L16,L17,L18,L19,L20,font, text_color)
        guess_box5 = self.draw_guessRow(x, y+220, width, height, screen, inputBox_color, L21,L22,L23,L24,L25,font, text_color)
        guess_box6 = self.draw_guessRow(x, y+275, width, height, screen, inputBox_color, L26,L27,L28,L29,L30,font, text_color)
        return guess_box,guess_box2,guess_box3,guess_box4,guess_box5,guess_box6

    def draw_colorBox(self,x,y,width,height,screen,box_color):
        box = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (box_color), box, 0)

    def backspace(self,L1,L2,L3,L4,L5,guess_1):
        guess_1 = guess_1[:-1]
        if len(guess_1) == 0:
            L1 = ''
        if len(guess_1) == 1:
            L2 = ''
        if len(guess_1) == 2:
            L3 = ''
        if len(guess_1) == 3:
            L4 = ''
        if len(guess_1) == 4:
            L5 = ''
        return L1,L2,L3,L4,L5,guess_1

    def write(self,L1,L2,L3,L4,L5,guess_1,guess_letters):
        
        for letter in guess_1:
            guess_letters += letter
        if len(guess_1) == 1:
            L1 = guess_letters[0]
        if len(guess_1) == 2:
            L2 = guess_letters[1]
        if len(guess_1) == 3:
            L3 = guess_letters[2]
        if len(guess_1) == 4:
            L4 = guess_letters[3]
        if len(guess_1) == 5:
            L5 = guess_letters[4]
        return L1,L2,L3,L4,L5,guess_1,guess_letters

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
                    self.wordle_screen(screen,username)
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

    def check_guess(self,word,guess,screen):
        word_letters = []
        guess_letters1 =[]
        colors = []
        num = 0
        x,y = 175,100
        dis=55

        for i in word:
            word_letters.append(i)
        print(f'WORD - {word_letters}')

        for i in guess:
            guess_letters1.append(i)
        print(f'GUESS - {guess_letters1}')
        
        
        for i in guess_letters1:
            if i == word_letters[num]:
                print('green')
                #self.draw_colorBox(x+dis,y,45,45,screen,(0,255,0))
                colors.append((0,255,0))
                dis+=55

            if i in word_letters:
                if i != word_letters[num]:
                    print('yellow')
                    colors.append((255,255,0))
                    #self.draw_colorBox(x+dis,y,45,45,screen,(255,0,255))
                    dis += 55
            if i not in word_letters:
                print('grey')
                colors.append((220,220,220))
                #self.draw_colorBox(x+dis,y,45,45,screen,(220,220,220))
                dis += 55

            num+=1 

        return colors

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
        lose_message = ''

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

    def wordle_screen(self,screen,username):
        error_message = ''
        win_message = ''
        lose_message = ''
        guess_1,guess_2,guess_3,guess_4,guess_5,guess_6 = '','','','','',''
        L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15,L16,L17,L18,L19,L20,L21,L22,L23,L24,L25,L26,L27,L28,L29,L30 = '','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
        letters = [L1,L2,L3,L4,L5,L6,L7,L8,L9,L10]
        click1 = False
        click2 = False
        running = True
        win = False
        lose = False
        R1_colors,R2_colors,R3_colors,R4_colors,R5_colors,R6_colors = [],[],[],[],[],[]
        line = 1
        guessed_words = []
        word = random.choice(words.WORDS)
        print(word)
        while running:

            guess_letters = []
            

            header_font = pygame.font.SysFont(None, 50)
            text_font = pygame.font.SysFont(None, 30)
            input_font = pygame.font.SysFont(None, 20)
            mx, my = pygame.mouse.get_pos()

            screen.fill(self.backgroundColor)
            self.draw_text('Wordle', header_font,self.textColor, screen, 20, 20)
            

            self.draw_text(error_message,text_font,(255,0,0),screen,200,475)
            self.draw_text(win_message,header_font,(0,250,0),screen,25,450)
            self.draw_text(lose_message,header_font,(255,0,0),screen,25,450)





            
            x,y = 175,105
            for i in R1_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55
            y+=55
            x= 175
            for i in R2_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55
            y+=55
            x= 175
            for i in R3_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55
            y+=55
            x= 175
            for i in R4_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55
            y+=55
            x= 175
            for i in R5_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55
            y+=55
            x= 175
            for i in R6_colors:
                self.draw_colorBox(x,y,45,45,screen,i)
                x+=55


            guess_tabel = self.draw_guessTable(175, 100, 50, 50, screen, (250,0,0), L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15,L16,L17,L18,L19,L20,L21,L22,L23,L24,L25,L26,L27,L28,L29,L30,header_font, self.textColor,line,outline =2)

            self.draw_keyboard(200,500,screen, (255,0,0), self.textColor,input_font)

            
            enter_button = self.draw_button(250, 700, 100, 50, screen, (255, 0, 0), 'Enter', text_font, self.textColor)

            back_button = self.draw_button(250, 800, 100, 50, screen, (255, 0, 0), 'Back', text_font, self.textColor)

            # Events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.exit_screen()

                if event.type == MOUSEBUTTONDOWN:
                    if back_button.collidepoint((mx, my)):
                        running = False
                    # if enter_button.collidepoint((mx, my)):
                    #     error_message = ''

                if event.type == pygame.KEYDOWN:
                    #if click1 == True:
                    if event.key == pygame.K_BACKSPACE:
                        if line == 1:
                            L1,L2,L3,L4,L5,guess_1 = self.backspace(L1,L2,L3,L4,L5,guess_1)
                        if line == 2:
                            L6,L7,L8,L9,L10,guess_2 = self.backspace(L6,L7,L8,L9,L10,guess_2)
                        if line == 3:
                            L11,L12,L13,L14,L15,guess_3 = self.backspace(L11,L12,L13,L14,L15,guess_3)
                        if line == 4:
                            L16,L17,L18,L19,L20,guess_4 = self.backspace(L16,L17,L18,L19,L20,guess_4)
                        if line == 5:
                            L21,L22,L23,L24,L25,guess_5 = self.backspace(L21,L22,L23,L24,L25,guess_5)
                        if line == 6:
                            L26,L27,L28,L29,L30,guess_6 = self.backspace(L26,L27,L28,L29,L30,guess_6)

                    elif event.key == pygame.K_RETURN:
                        if win == True:
                            self.wordle_screen(screen,username)
                        if lose == True:
                            self.wordle_screen(screen,username)
                        
                        if line ==1:
                            if len(guess_1) == 5:
                                if guess_1 in words.WORDS:
                                    if guess_1 not in guessed_words:
                                        if guess_1 != word:
                                            R1_colors = self.check_guess(word,guess_1,screen)
                                            guessed_words.append(guess_1)
                                            line += 1
                                        else:
                                            R1_colors = self.check_guess(word,guess_1,screen)
                                            guessed_words.append(guess_1)
                                            win = True

                                            # if guess_1 == word:
                                            #     line += 1
                                            # else:
                                            #     win = True    
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'
                                    
                        if line ==2:
                            if len(guess_2) == 5:
                                if guess_2 in words.WORDS:
                                    if guess_2 not in guessed_words:
                                        if guess_2 != word:
                                            R2_colors = self.check_guess(word,guess_2,screen)
                                            guessed_words.append(guess_2)
                                            line += 1
                                        else:
                                            R2_colors = self.check_guess(word,guess_2,screen)
                                            guessed_words.append(guess_2)
                                            win = True
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'
                        if line ==3:
                            if len(guess_3) == 5:
                                if guess_3 in words.WORDS:
                                    if guess_3 not in guessed_words:
                                        if guess_3 != word:
                                            R3_colors = self.check_guess(word,guess_3,screen)
                                            guessed_words.append(guess_3)
                                            line += 1
                                        else:
                                            R3_colors = self.check_guess(word,guess_3,screen)
                                            guessed_words.append(guess_3)
                                            win = True
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'

                        if line ==4:
                            if len(guess_4) == 5:
                                if guess_4 in words.WORDS:
                                    if guess_4 not in guessed_words:
                                        if guess_4 != word:
                                            R4_colors = self.check_guess(word,guess_4,screen)
                                            guessed_words.append(guess_4)
                                            line += 1
                                        else:
                                            R4_colors = self.check_guess(word,guess_4,screen)
                                            guessed_words.append(guess_4)
                                            win = True
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'

                        if line ==5:
                            if len(guess_5) == 5:
                                if guess_5 in words.WORDS:
                                    if guess_5 not in guessed_words:
                                        if guess_5 != word:
                                            R5_colors = self.check_guess(word,guess_5,screen)
                                            guessed_words.append(guess_5)
                                            line += 1
                                        else:
                                            R5_colors = self.check_guess(word,guess_5,screen)
                                            guessed_words.append(guess_5)
                                            win = True
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'
                        if line ==6:
                            if len(guess_6) == 5:
                                if guess_6 in words.WORDS:
                                    if guess_6 not in guessed_words:
                                        if guess_6 != word:
                                            R6_colors = self.check_guess(word,guess_6,screen)
                                            guessed_words.append(guess_6)
                                            lose_message = 'Unlcuky - press enter to play again'
                                            lose = True
                                        else:
                                            R6_colors = self.check_guess(word,guess_6,screen)
                                            guessed_words.append(guess_6)
                                            win = True
                                            # if guess_1 == word:
                                            #     line += 1
                                            # else:
                                            #     win = True    
                                    else:
                                        error_message = ''
                                        error_message = 'Cant guess that again'
                                else:
                                    
                                    error_message = ''
                                    error_message = 'Thats not a word'
                                
                    else:
                        if line == 1:
                            if len(guess_1) != 5:
                                guess_1 += event.unicode
                                L1,L2,L3,L4,L5,guess_1,guess_letters = self.write(L1,L2,L3,L4,L5,guess_1,guess_letters)
                        if line == 2:
                            if len(guess_2) != 5:
                                guess_2 += event.unicode
                                L6,L7,L8,L9,L10,guess_2,guess_letters = self.write(L6,L7,L8,L9,L10,guess_2,guess_letters)
                        if line == 3:
                            if len(guess_3) != 5:
                                guess_3 += event.unicode
                                L11,L12,L13,L14,L15,guess_3,guess_letters = self.write(L11,L12,L13,L14,L15,guess_3,guess_letters)
                        if line == 4:
                            if len(guess_4) != 5:
                                guess_4 += event.unicode
                                L16,L17,L18,L19,L20,guess_4,guess_letters = self.write(L16,L17,L18,L19,L20,guess_4,guess_letters)
                        if line == 5:
                            if len(guess_5) != 5:
                                guess_5 += event.unicode
                                L21,L22,L23,L24,L25,guess_5,guess_letters = self.write(L21,L22,L23,L24,L25,guess_5,guess_letters)
                        if line == 6:
                            if len(guess_6) != 5:
                                guess_6 += event.unicode
                                L26,L27,L28,L29,L30,guess_6,guess_letters = self.write(L26,L27,L28,L29,L30,guess_6,guess_letters)
                                

                    if click2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        elif event.key == pygame.K_RETURN:
                            password = password
                        else:
                            password += event.unicode
                    # if event.key == pygame.K_RETURN:
                    #     error_message = ''

                    if win == True:
                        error_message = ''
                        win_message = 'You Won - Press Enter to play again'
                        


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