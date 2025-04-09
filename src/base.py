# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)



#game状态

GAME_LOG_EVENT = True
GAME_LOG_EVENT_LEVEL = 'WARNING'
GAME_LOG_EVENT_SHOWCONSOLE = False


GAME_STAUTS_RUNNING = 1
GAME_STATUS_OVER = 2
GAME_STATUS_CLOSE = 3

GAME_SCREEN_WIDTH = 800
GAME_SCREEN_HEIGHT = 600



#ENTITY
"""三个id值起始位置"""
PLAYER_ID_BEGIN = 0
ENEMY_ID_BEGIN = 16
BULLET_ID_BEGIN = 512
ENTITY_ID_END = 1024

PLAYER_ACCELERATION = 0.5 #加速度
PLAYER_MAX_SPEED = 10
PLAYER_PLANE_WEIGHT = 880 #0.88 Ton
PLAYER_BODY_COLOR = (0,100,255)
PLAYER_BODYSIZE_X = 30
PLAYER_BODYSIZE_Y = 40
PLAYER_ALLOW_EXCEED_MAX_SPEED = False

ENEMY_ACCELERATION = 0.5 #加速度
ENEMY_MAX_SPEED = 6
ENEMY_PLANE_WEIGHT = 1120 #0.88 Ton
ENEMY_BODY_COLOR = (255, 0, 0) #red
ENEMY_BODYSIZE_X = 40
ENEMY_BODYSIZE_Y = 60
ENEMY_ALLOW_EXCEED_MAX_SPEED = False

BULLET_INITIAL_SPEED = 50
BULLET_ACCELERATION = 0.5 #加速度
BULLET_MAX_SPEED = 400
BULLET_BODY_COLOR = (255,255,255)
BULLET_BODYSIZE_X = 4
BULLET_BODYSIZE_Y = 8
BULLET_ALLOW_EXCEED_MAX_SPEED = True #是否允许超速
BULLET_STOP_SPEED_THRESHOLD = 0.5 #当速度小于该值时判定为停止



#环境
ENVIRONMENT_AIR_DENSITY = 0.9 #等同于摩擦系数(0-1)



def is_out_of_screen(x:int=0,y:int=0)->bool:
    if(x>GAME_SCREEN_WIDTH or y>GAME_SCREEN_HEIGHT or x<0 or y<0):
        return True
    return False
