#Imports
import pygame
from pygame import font
from sys import exit
import random

#Classes
class PaddleOne(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('paddle.png')
        self.rect = self.image.get_rect(center=(30, 300))
    def paddle_one_move(self):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.rect.y -= 7
            elif keys[pygame.K_s]:
                self.rect.y += 7
        if self.rect.y <= 30:
            self.rect.y = 30
        elif self.rect.y >= 500:
            self.rect.y = 500


    def update(self):
        self.paddle_one_move()

class PaddleTwo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('paddle.png')
        self.rect = self.image.get_rect(center=(770, 300))

    def paddle_two_move(self):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.rect.y -= 7
            elif keys[pygame.K_DOWN]:
                self.rect.y += 7

            if self.rect.y <= 30:
                self.rect.y = 30
            elif self.rect.y >= 500:
                self.rect.y = 500
    def update(self):
        self.paddle_two_move()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ball.png')
        self.rect = self.image.get_rect(center=(400, 300))
        self.speed_x = 3
        self.speed_y = 3
        self.score_sound = pygame.mixer.Sound('jumpsound.wav')
        self.score_sound.set_volume(0.5)

    def move_ball(self):
        global player1_score
        global player2_score
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y <= 30 or self.rect.y >= 575:
            self.speed_y *= -1
        if self.rect.x >= 800:
            player1_score += 1
            self.rect.x = 400
            self.rect.y = 300
            self.speed_x *= -1
            self.score_sound.play()

        if self.rect.x <= 0:
            player2_score += 1
            self.rect.x = 400
            self.rect.y = 300
            self.speed_x *= -1
            self.score_sound.play()

    def ball_collision(self):

        if pygame.sprite.spritecollide(paddle1.sprite,ball,False):
            self.speed_x *= -1
        elif pygame.sprite.spritecollide(paddle2.sprite,ball, False):
            self.speed_x *= -1

    def update(self):
        self.move_ball()
        self.ball_collision()
#Functions
def scoreboard():
    global player1_score
    global player2_score
    global game_running
    score_screen1 = new_font.render(f'{player1_score}',False,(255,255,255))
    score_rect1 = score_screen1.get_rect(center=(10, 20))
    screen.blit(score_screen1, score_rect1)
    score_screen2 = new_font.render(f'{player2_score}',False,(255,255,255))
    score_rect2 = score_screen2.get_rect(center=(780,20))
    screen.blit(score_screen2, score_rect2)
    if player2_score == 10 or player1_score == 10:
        game_running = False

#Initialization
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")
timer = pygame.time.Clock()
pygame.init()

#Essential Variables
game_running = True
pygame.key.set_repeat(True)
player1_score = 0
player2_score = 0

#Assets
new_font = pygame.font.Font('Pixeltype.ttf', 50)

background_img = pygame.image.load('pongBG.png')

paddle1 = pygame.sprite.GroupSingle()
paddle1.add(PaddleOne())

paddle2 = pygame.sprite.GroupSingle()
paddle2.add(PaddleTwo())


ball = pygame.sprite.GroupSingle()
ball.add(Ball())

#Game Loop
while True:
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_running:
        screen.fill("White")
        screen.blit(background_img, (0,0))
        scoreboard()
        paddle1.draw(screen)
        paddle1.update()
        paddle2.draw(screen)
        paddle2.update()
        ball.draw(screen)
        ball.update()
    else:
        screen.fill("Black")
        score = 0
        if player2_score > player1_score:
            score = player2_score
            score_screen_final = new_font.render('Player 2 wins', False, (255, 255, 255))
            score_rect_final = score_screen_final.get_rect(center=(400, 300))

        else:
            score = player1_score
            score_screen_final = new_font.render('Player 1 wins', False, (255, 255, 255))
            score_rect_final = score_screen_final.get_rect(center=(400, 300))

        retry_screen = new_font.render('Press ENTER to play again', False, (255, 255, 255))
        retry_rect = retry_screen.get_rect(center =(400,350))
        screen.blit(score_screen_final, score_rect_final)
        screen.blit(retry_screen,retry_rect)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_running = True
                player1_score = 0
                player2_score = 0


    pygame.display.update()
    timer.tick(60)
