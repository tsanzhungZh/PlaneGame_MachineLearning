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
        self.color = (0, 100, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.PLAYER_BODYSIZE_X / 2
        self.radius_y = base.PLAYER_BODYSIZE_Y / 2

        self.id = 0
        self.health = 1
        self.attack = 1

        self.x = 0
        self.y = 0

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5  # 加速度
        self.allow_exceed_max_speed = False
        self.max_speed = 5  # 最大速度
        self.friction = 0.95  # 摩擦系数(0-1)



        self.rect.x = self.x
        self.rect.y = self.y

        self._init_event_cb()

    def calculate_pos(self):
        # 限制最大速度
        if(self.allow_exceed_max_speed == False):
            speed = (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
            if speed > self.max_speed:
                scale = self.max_speed / speed
                self.velocity_x *= scale
                self.velocity_y *= scale

        # 应用摩擦力(逐渐减速)
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        # 如果速度很小，直接设为0
        if abs(self.velocity_x) < 0.1: self.velocity_x = 0
        if abs(self.velocity_y) < 0.1: self.velocity_y = 0

        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 边界检查
        self.x = max(self.radius_x, min(self.x, base.GAME_SCREEN_WIDTH - self.radius_x))
        self.y = max(self.radius_y, min(self.y, base.GAME_SCREEN_HEIGHT - self.radius_y))

        self.rect.x = self.x
        self.rect.y = self.y


    def update(self, *args, **kwargs):
        self.event_handler()
        self.calculate_pos()
        #self.rect.x += self.promoting_acc_x
    def set_id(self,id:int)->int:
        """return old id"""
        old_id = self.id
        self.id = id
        return old_id

    def shoot(self):
        """发送一个玩家射击的事件"""
        ev = event.Event()
        ev.set_event_name(event.NAME_PLAYER_SHOOT)
        event.EventControler.send_event(ev)
    """
    def calculate_pos2(self):

        print("cal pos")
        #更新摩擦力
        self.friction_acc_x = 1 / 2  * abs(self.speed_x) ** 2
        self.friction_acc_y = 1 / 2  * abs(self.speed_y) ** 2

        if(self.speed_x>0):
            self.friction_acc_x = -self.friction_acc_x
        if(self.speed_y>0):
            self.friction_acc_y = -self.friction_acc_y

        #更新acc
        self.accelerate_x = self.promoting_acc_x + self.friction_acc_x
        self.accelerate_y = self.promoting_acc_y + self.friction_acc_y
        print(self.accelerate_x)
        print(self.accelerate_y)


        self.speed_x += self.accelerate_x
        self.speed_y += self.accelerate_y
        print(self.speed_x)
        print(self.speed_y)
        # 超速检测
        '''
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
        '''
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.promoting_acc_x = 0
        self.promoting_acc_y = 0
    """

    """
    ==================== EVENT HANDLER and CALLBACK ========================
    """
    def event_handler(self):
        pass

    def _init_event_cb(self):
        event.EventControler.add_subscriber(event.NAME_USER_CONTINUES_INPUT, self.cb_player_move)
        event.EventControler.add_subscriber(event.NAME_USER_CONTINUES_INPUT, self.cb_player_shoot)

    def cb_player_move(self,ev : event.Event)->None:
        # 加速度计算
        keys = ev.keys
        if keys[pygame.K_a]:
            self.velocity_x -= self.acceleration
        if keys[pygame.K_d]:
            self.velocity_x += self.acceleration
        if keys[pygame.K_w]:
            self.velocity_y -= self.acceleration
        if keys[pygame.K_s]:
            self.velocity_y += self.acceleration

        """ 禁用单键用户输入
        if(ev.event_name == event.NAME_USER_INPUT):
            if(ev.key == event.K_a):
                print("key_player__AAAAAAA")
                self.promoting_acc_x = -self.promoting_force_x
            elif(ev.key == event.K_d):
                self.promoting_acc_x = self.promoting_force_x
            elif(ev.key == event.K_w):
                self.promoting_acc_x = -self.promoting_force_y
            elif(ev.key == event.K_s):
                self.promoting_acc_x = self.promoting_force_y
        """


    def cb_player_shoot(self,ev : event.Event)->None:
        if(ev.event_name == event.NAME_USER_INPUT):
            if(ev.key == event.K_SPACE):
                self.shoot()
    def cb_player_hit(self,ev : event.Event)->None:
        pass

class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 40))
        self.color = (0, 100, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.PLAYER_BODYSIZE_X / 2
        self.radius_y = base.PLAYER_BODYSIZE_Y / 2

        self.id = 0
        self.health = 1
        self.attack = 1

        self.x = 0
        self.y = 0

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5  # 加速度
        self.max_speed = 5  # 最大速度
        self.friction = 0.95  # 摩擦系数(0-1)

        self.rect.x = self.x
        self.rect.y = self.y

        self._init_event_cb()

    def _init_event_cb(self):
        pass

    def update(self):
        """出界检查"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 40))
        self.color = (0, 100, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.PLAYER_BODYSIZE_X / 2
        self.radius_y = base.PLAYER_BODYSIZE_Y / 2

        self.id = 0
        self.health = 1
        self.attack = 1

        self.x = 0
        self.y = 0

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5  # 加速度
        self.max_speed = 5  # 最大速度
        self.friction = 0.95  # 摩擦系数(0-1)

        self.rect.x = self.x
        self.rect.y = self.y

        self._init_event_cb()

    def _init_event_cb(self):
        pass
    def update(self):
        pass

class EntityControler:
    #group


    g_all_entityGroup = pygame.sprite.Group()
    g_playerGroup = pygame.sprite.Group()
    g_enemyGroup = pygame.sprite.Group()
    g_bulletGroup = pygame.sprite.Group()

    @staticmethod
    def update():
        EntityControler.p_collision_judgment()
        EntityControler.g_all_entityGroup.update()

    @staticmethod
    def draw(screen):
        EntityControler.g_all_entityGroup.draw(screen)

    def __new__(cls):
        return None

    @staticmethod
    def init():
        pass

    @staticmethod
    def init_group():
        pass




    @staticmethod
    def add_new_player(x:int=0,y:int=0)->int:
        ply = Player()
        ply.x = x
        ply.y = y
        EntityControler.g_all_entityGroup.add(ply)
        EntityControler.g_playerGroup.add(ply)
        return len(EntityControler.g_playerGroup)

    @staticmethod
    def get_player(player_id:int=0)->Player:
        for player in EntityControler.g_playerGroup:
            if(player.id == player_id):
                return player
        return None

    @staticmethod
    def modify_player_attribute(ply:Player=None,ply_id=0,attribute:dict= {'default':1})->bool:
        if(ply==None):
            player = EntityControler.get_player(player_id=ply_id)
        else:
            player = ply
        for k in attribute.keys():
            if(k == 'x'):
                player.x = attribute.get(k)
            elif(k == 'y'):
                player.y = attribute.get(k)
            elif (k == 'velocity_x'):
                player.velocity_x = attribute.get(k)
            elif (k == 'velocity_y'):
                player.velocity_y = attribute.get(k)
            elif(k == 'allow_exceed_max_speed'):
                player.allow_exceed_max_speed = attribute.get(k)



        return True

    @staticmethod
    def set_player_pos(x:int=0,y:int=0,ply:Player=None,ply_id:int=0):
        if(ply==None):
            for player in EntityControler.g_playerGroup:
                if(player.id == ply_id):
                    player.x = x
                    player.y = y
        else:
            ply.x = x
            ply.y = y

    def _set_entity_pos( x :int=0,y:int=0,et=None,et_id:int=0):
        if(et == None):
            for entity in EntityControler.g_all_entityGroup:
                if(entity.id == et_id):
                    entity.x = x
                    entity.y = y
        else:
            et.x = x
            et.y = y



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
    def p_collision_judgment():

        """player collisions judgement (with enemy)"""
        player_collisions = pygame.sprite.groupcollide(EntityControler.g_playerGroup,EntityControler.g_enemyGroup,False,False)
        for player,enemies in player_collisions:
            ev = event.Event(player_id=player.id,type=event.TYPE_ENVIRONMENT,event_name=event.NAME_ENVIRONMENT_COLLISION_P_E)
            event.EventControler.send_event(ev)

        """enemy collisions judgement (with bullet)"""
        enemy_collisions = pygame.sprite.groupcollide(EntityControler.g_bulletGroup,EntityControler.g_enemyGroup,False,False)
        for bullet,enemies in enemy_collisions:
            for enemy in enemies:
                ev = event.Event(enemy_id=enemy.id,bullet_id=bullet.id,type=event.TYPE_ENVIRONMENT,event_name=event.NAME_ENVIRONMENT_COLLISION_B_E)
                event.EventControler.send_event(ev)

