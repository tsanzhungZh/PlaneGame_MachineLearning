import pygame
import random
import sys
import base
import event

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((base.PLAYER_BODYSIZE_X, base.PLAYER_BODYSIZE_Y))
        self.color = base.PLAYER_BODY_COLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.PLAYER_BODYSIZE_X / 2
        self.radius_y = base.PLAYER_BODYSIZE_Y / 2

        self.id = base.PLAYER_ID_BEGIN
        self.health = 1
        self.attack = 1

        self.x = 0
        self.y = 0

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = base.PLAYER_ACCELERATION  # 加速度
        self.allow_exceed_max_speed = base.PLAYER_ALLOW_EXCEED_MAX_SPEED
        self.max_speed = base.PLAYER_MAX_SPEED  # 最大速度
        self.friction = base.ENVIRONMENT_AIR_DENSITY  # 摩擦系数(0-1)



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
        #self.x = max(self.radius_x, min(self.x, base.GAME_SCREEN_WIDTH - self.radius_x))
        #self.y = max(self.radius_y, min(self.y, base.GAME_SCREEN_HEIGHT - self.radius_y))
        self.x = max(0, min(self.x, base.GAME_SCREEN_WIDTH))
        self.y = max(0, min(self.y, base.GAME_SCREEN_HEIGHT))




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
        ev.set_event_type(event.TYPE_PLAYER)
        ev.set_event_name(event.NAME_PLAYER_SHOOT)
        ev.player_id = self.id
        event.EventControler.send_event(ev)

    """
    ==================== EVENT HANDLER and CALLBACK ========================
    """
    def event_handler(self):
        pass

    def _init_event_cb(self):
        event.EventControler.add_subscriber(event.NAME_USER_CONTINUES_INPUT, self.cb_player_move)
        event.EventControler.add_subscriber(event.NAME_USER_INPUT, self.cb_player_shoot)

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
            if(ev.key == event.K_SPACE and ev.type == event.TYPE_KEYDOWN):
                self.shoot()

    def cb_player_hit(self,ev : event.Event)->None:
        """击中目标事件"""
        pass

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.Surface((base.BULLET_BODYSIZE_X, base.BULLET_BODYSIZE_Y))
        self.color = base.BULLET_BODY_COLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.BULLET_BODYSIZE_X / 2
        self.radius_y = base.BULLET_BODYSIZE_Y / 2

        self.id = base.BULLET_ID_BEGIN
        self.owner_id = 0
        self.health = 1
        self.attack = 1

        self.x = x
        self.y = y

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = base.BULLET_ACCELERATION  # 加速度
        self.allow_exceed_max_speed = base.BULLET_ALLOW_EXCEED_MAX_SPEED
        self.max_speed = base.BULLET_MAX_SPEED  # 最大速度
        self.friction = base.ENVIRONMENT_AIR_DENSITY  # 摩擦系数(0-1)

        self.is_stop = False
        self.moving_status_changed = True

        self.rect.x = self.x
        self.rect.y = self.y

        self._init_event_cb()




    def calculate_pos(self):
        """出界检查"""
        # 限制最大速度
        if (self.allow_exceed_max_speed == False):
            speed = (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
            if speed > self.max_speed:
                scale = self.max_speed / speed
                self.velocity_x *= scale
                self.velocity_y *= scale

        # 应用摩擦力(逐渐减速)
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        # 如果速度很小，直接设为0
        if abs(self.velocity_x) < base.BULLET_STOP_SPEED_THRESHOLD: self.velocity_x = 0
        if abs(self.velocity_y) < base.BULLET_STOP_SPEED_THRESHOLD: self.velocity_y = 0

        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 边界检查
        self.x = max(self.radius_x, min(self.x, base.GAME_SCREEN_WIDTH - self.radius_x))
        self.y = max(self.radius_y, min(self.y, base.GAME_SCREEN_HEIGHT - self.radius_y))


        self.rect.x = self.x
        self.rect.y = self.y


        if(self.velocity_x == self.velocity_y == 0):
            if(self.is_stop == False):
                self.is_stop = True
                self.moving_status_changed = True
            else:
                self.moving_status_changed = False
        else:
            if(self.is_stop == True):
                self.is_stop = False
                self.moving_status_changed = True
            else:
                self.moving_status_changed = False


    def check_move(self):
        if(self.moving_status_changed == True):
            self.moving_status_changed = False

            ev = event.Event()
            ev.set_event_type(event.TYPE_BULLET)
            ev.set_event_name(event.NAME_BULLET_STOP)
            ev.bullet_id = self.id
            ev.player_id = self.owner_id
            print(f"blt id {self.id}")
            event.EventControler.send_event(ev)


    def update(self):
        self.calculate_pos()
        self.check_move()



    def _init_event_cb(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((base.ENEMY_BODYSIZE_X, base.ENEMY_BODYSIZE_Y))
        self.color = base.ENEMY_BODY_COLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.radius_x = base.ENEMY_BODYSIZE_X / 2
        self.radius_y = base.ENEMY_BODYSIZE_Y / 2

        self.id = base.ENEMY_ID_BEGIN
        self.health = 1
        self.attack = 1

        self.x = 0
        self.y = 0

        # 运动参数
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = base.ENEMY_ACCELERATION  # 加速度
        self.allow_exceed_max_speed = base.ENEMY_ALLOW_EXCEED_MAX_SPEED
        self.max_speed = base.ENEMY_MAX_SPEED  # 最大速度
        self.friction = base.ENVIRONMENT_AIR_DENSITY  # 摩擦系数(0-1)

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
        #self.x = max(self.radius_x, min(self.x, base.GAME_SCREEN_WIDTH - self.radius_x))
        #self.y = max(self.radius_y, min(self.y, base.GAME_SCREEN_HEIGHT - self.radius_y))

        self.x = max(0, min(self.x, base.GAME_SCREEN_WIDTH))
        self.y = max(0, min(self.y, base.GAME_SCREEN_HEIGHT))


        self.rect.x = self.x
        self.rect.y = self.y




    """=====================event call back ==========================="""
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

    g_id_pool = set()
    @staticmethod
    def update():
        EntityControler._collision_judgment()
        EntityControler.g_all_entityGroup.update()

    @staticmethod
    def draw(screen):
        EntityControler.g_all_entityGroup.draw(screen)

    def __new__(cls):
        return None

    @staticmethod
    def init():
        EntityControler._init_event_cb()
        EntityControler.init_group()
        EntityControler.init_entity_logger()

    @staticmethod
    def init_group():
        pass

    @staticmethod
    def init_entity_logger():
        pass

    @staticmethod
    def _alloc_id(begin=base.PLAYER_ID_BEGIN,end=base.ENTITY_ID_END):
        for i in range(begin,end):
            if i in EntityControler.g_id_pool:
                continue
            else:
                EntityControler.g_id_pool.add(i)
                print(f"alloc id{i}")
                return i



    """=====-----<<<<< player operation >>>>>-----====="""
    @staticmethod
    def add_new_player(x:int=0,y:int=0)->int:
        ply = Player()
        ply.x = x
        ply.y = y
        EntityControler.g_all_entityGroup.add(ply)
        EntityControler.g_playerGroup.add(ply)

        ply_id = EntityControler._alloc_id(base.PLAYER_ID_BEGIN,base.ENEMY_ID_BEGIN)
        EntityControler.g_id_pool.add(ply_id)

        return len(EntityControler.g_playerGroup)

    @staticmethod
    def add_new_bullet(x:int=0,y:int=0,v:int=base.BULLET_INITIAL_SPEED)->int:

        blt = Bullet(x + base.PLAYER_BODYSIZE_X/2,y)
        blt.velocity_y = -v
        blt.velocity_x = 0

        blt_id = EntityControler._alloc_id(base.BULLET_ID_BEGIN, base.ENTITY_ID_END)
        blt.id = blt_id

        EntityControler.g_id_pool.add(blt_id)
        EntityControler.g_all_entityGroup.add(blt)
        EntityControler.g_bulletGroup.add(blt)


        return len(EntityControler.g_bulletGroup)

    @staticmethod
    def _remove_entity(id:int = 0)->bool:

        if(id not in EntityControler.g_id_pool):
            return False

        """add log"""

        for et in EntityControler.g_all_entityGroup:
            if(et.id == id):
                et.kill()
                EntityControler.g_id_pool.remove(et.id)
                return True
        return False

    @staticmethod
    def _get_entity(id:int = 0):
        for et in EntityControler.g_all_entityGroup:
            if(et.id == id):
                return et
        return None

    @staticmethod
    def get_player(player_id:int=0)->Player:
        for player in EntityControler.g_playerGroup:
            if(player.id == player_id):
                return player
        return None

    @staticmethod
    def modify_entity_attribute(entity=None, entity_id=0, attribute:dict= {'default':1})->bool:
        ret = True
        if(entity==None):
            et = EntityControler._get_entity(id=entity_id)
        else:
            et = entity
        for k in attribute.keys():
            if(k == 'x'):
                et.x = attribute.get(k)
            elif(k == 'y'):
                et.y = attribute.get(k)
            elif (k == 'velocity_x'):
                et.velocity_x = attribute.get(k)
            elif (k == 'velocity_y'):
                et.velocity_y = attribute.get(k)
            elif(k == 'allow_exceed_max_speed'):
                et.allow_exceed_max_speed = attribute.get(k)
            else:
                ret = False

        return ret

    @staticmethod
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
    def set_player_pos(x: int = 0, y: int = 0, ply: Player = None, ply_id: int = 0):

        try:
            EntityControler._set_entity_pos(x, y, ply, ply_id)
        except Exception as e:  # 捕获所有异常
            if (ply == None):
                for player in EntityControler.g_playerGroup:
                    if (player.id == ply_id):
                        player.x = x
                        player.y = y
            else:
                ply.x = x
                ply.y = y

    @staticmethod
    def set_bullet_pos(x: int = 0, y: int = 0, blt: Bullet = None, blt_id: int = 0):
        EntityControler._set_entity_pos(x, y, blt, blt_id)
    def set_enemy_pos(x: int = 0, y: int = 0, enemy: Enemy = None, enemy_id: int = 0):

        EntityControler._set_entity_pos(x, y, enemy, enemy_id)

    @staticmethod
    def _collision_judgment():

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

    @staticmethod
    def _init_event_cb():
        event.EventControler.add_subscriber(event.NAME_BULLET_STOP,EntityControler.cb_bullet_stop)
        event.EventControler.add_subscriber(event.NAME_PLAYER_SHOOT, EntityControler.cb_player_shoot)

    @staticmethod
    def cb_player_shoot(ev:event.Event):
        if(ev.event_name == event.NAME_PLAYER_SHOOT):
            player = EntityControler.get_player(ev.player_id)
            x = player.x
            y = player.y
            EntityControler.add_new_bullet(x,y)

    @staticmethod
    def cb_bullet_stop(ev:event.Event):
        if(ev.event_name== event.NAME_BULLET_STOP):
            blt_id = ev.bullet_id

            if(True == EntityControler._remove_entity(blt_id)):

                ev = event.Event()
                ev.set_event_type(event.TYPE_BULLET)
                ev.set_event_name(event.NAME_BULLET_DEAD)
                event.EventControler.send_event(ev)
