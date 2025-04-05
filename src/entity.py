import pygame
import random
import sys
import base
import event

class Player(pygame.sprite.Sprite):

    s_Player_max_speed = base.PLAYER_MAX_SPEED

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 40))
        self.image.fill(base.WHITE)
        self.rect = self.image.get_rect()

        self.id = 0
        self.health = 1
        self.attack = 1

        self.promoting_force_x = 10
        self.promoting_force_y = 5

        self.promoting_acc_x = 0
        self.promoting_acc_y = 0

        self.friction_acc_x = 0
        self.friction_acc_y = 0

        self.accelerate_x = 0
        self.accelerate_y = 0

        self.speed_x = 0
        self.speed_y = 0



    def update(self, *args, **kwargs):
        self.event_handler()
        self.calculate_pos()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)

    def calculate_pos(self):

        #更新摩擦力
        self.friction_acc_x = int(1 / 2  * abs(self.speed_x) ** 2)
        self.friction_acc_y = int(1 / 2  * abs(self.speed_y) ** 2)
        if(self.speed_x>=0):
            self.friction_acc_x = -self.friction_acc_x
        if(self.speed_y>=0):
            self.friction_acc_y = -self.friction_acc_y

        #更新acc
        self.accelerate_x = self.promoting_acc_x + self.friction_acc_x
        self.accelerate_y = self.promoting_acc_y + self.friction_acc_y

        self.speed_x += self.accelerate_x
        self.speed_y += self.accelerate_y

        # 超速检测
        if (abs(self.speed_x) > base.PLAYER_MAX_SPEED):
            if (self.speed_x > 0):
                self.speed_x = base.PLAYER_MAX_SPEED
            else:
                self.speed_x = -base.PLAYER_MAX_SPEED
        if (abs(self.speed_y) > base.PLAYER_MAX_SPEED):
            if (self.speed_y > 0):
                self.speed_y = base.PLAYER_MAX_SPEED
            else:
                self.speed_y = -base.PLAYER_MAX_SPEED

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y





    """
    ==================== EVENT HANDLER and CALLBACK ========================
    """
    def event_handler(self):
        pass

    def init_event_cb(self):
        event.EventControler.add_subscriber(event.NAME_USER_INPUT, self.cb_player_move)
    def cb_player_move(self,ev : event.Event)->None:
        if(ev.event_name == event.NAME_USER_INPUT):
            if(ev.key == event.K_a):
                self.promoting_acc_x = -self.promoting_force_x
            elif(ev.key == event.K_d):
                self.promoting_acc_x = self.promoting_force_x
            elif(ev.key == event.K_w):
                self.promoting_acc_x = -self.promoting_force_y
            elif(ev.key == event.K_s):
                self.promoting_acc_x = self.promoting_force_y
            elif(ev.key == event.K_SPACE):
                pass





class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(base.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        """出界检查"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

