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

    def set_id(self,id:int)->int:
        """return old id"""
        old_id = self.id
        self.id = id
        return old_id

    def shoot(self):
        """发送一个玩家射击的事件"""
        ev = event.Event()
        ev.set_event_name(event.NAME_PLAYER_SHOOT)
        event.EventControler.event_game_send(ev)

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
        event.EventControler.add_subscriber(event.NAME_USER_INPUT, self.cb_player_shoot)

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
    def cb_player_shoot(self,ev : event.Event)->None:
        if(ev.event_name == event.NAME_USER_INPUT):
            if(ev.key == event.K_SPACE):
                self.shoot()
    def cb_player_hit(self,ev : event.Event)->None:
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

        self.id = 0

    def update(self):
        """出界检查"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 60))
        self.image.fill(base.RED)
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
    def update(self):
        pass

class EntityControler:
    #group


    g_all_entityGroup = pygame.sprite.Group()
    g_playerGroup = pygame.sprite.Group()
    g_enemyGroup = pygame.sprite.Group()
    g_bulletGroup = pygame.sprite.Group()
    #
    @staticmethod
    def update():
        EntityControler.collision_judgment()

    def __new__(cls):
        return None
    @staticmethod
    def init_group():
        pass

    @staticmethod
    def add_new_player(ply:Player)->None:
        EntityControler.g_all_entityGroup.add(ply)
        EntityControler.g_playerGroup.add(ply)
        pass
    @staticmethod
    def add_new_enemy(enemy:Enemy) -> None:
        EntityControler.g_all_entityGroup.add(enemy)
        EntityControler.g_enemyGroup.add(enemy)
        pass
    @staticmethod
    def add_new_bullet(bullet: Bullet) -> None:
        EntityControler.g_all_entityGroup.add(bullet)
        EntityControler.g_bulletGroup(bullet)
        pass

    @staticmethod
    def collision_judgment():
        """player collisions judgement (with enemy)"""
        player_collisions = pygame.sprite.groupcollide(EntityControler.g_playerGroup,EntityControler.g_enemyGroup,False,False)
        for player,enemies in player_collisions:
            ev = event.Event(player_id=player.id,type=event.TYPE_ENVIRONMENT,event_name=event.NAME_ENVIRONMENT_COLLISION_P_E)
            event.EventControler.event_game_send(ev)

        """enemy collisions judgement (with bullet)"""
        enemy_collisions = pygame.sprite.groupcollide(EntityControler.g_bulletGroup,EntityControler.g_enemyGroup,False,False)
        for bullet,enemies in enemy_collisions:
            for enemy in enemies:
                ev = event.Event(enemy_id=enemy.id,type=event.TYPE_ENVIRONMENT,event_name=event.NAME_ENVIRONMENT_COLLISION_P_E)










