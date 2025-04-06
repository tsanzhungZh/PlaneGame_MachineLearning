import queue
import logger
import pygame
import random
import sys
from queue import Queue
import base
#other constants
MAX_EVENT_RECEPTION_NUMS = 1024

class Event:
    """"""
    # 类属性（所有实例共享）
    priority = 0xff
    type = -1 #好几种，除了600000和600001分别对应敌人和环境事件，其他都以pygame为准,只能在初始化时设置
    key = -1 #输入事件时的按键值，非输入事件时默认-1,用户不可设置
    event_name = -1 #自定义事件的事件名，具体序号查表
    #id
    enemy_id = -1 #敌人发送事件时的id标识
    player_id = -1#玩家id(多人游戏时可以加以区分)

    # 初始化方法（构造函数）
    def __init__(self,type=-1,key=-1,event_name = -1,player_id = -1,enemy_id=-1,bullet_id=-1,priority = 0xff):

        self.type = type  # 实例属性
        self.key = key

        self.keys = None

        self.priority = priority

        self.event_name = event_name
        self.enemy_id = enemy_id
        self.player_id = player_id
        self.bullet_id = bullet_id

    def __del__(self):
        pass
    def set_event_name(self,ev_name):
        self.event_name = ev_name
    def set_enemy_id(self,id):
        self.enemy_id = id
    def set_player_id(self,id):
        self.player_id = id

class PubSub:
    """订阅器模块"""
    def __init__(self):
        self._subscribers = {}  # 事件名: [回调函数1, 回调函数2, ...]

    def subscribe(self, event_name, callback):
        """订阅事件"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def publish(self, event_name, *args, **kwargs):
        """发布事件"""
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)


class EventControler:
    """key range used for event log """
    s_log_event_counter = 0
    s_log_event_switch = base.GAME_LOG_EVENT
    s_event_logger = None

    """0关闭 1空闲中 2处理中    """
    s_status = 1
    """moduler reception"""
    s_event_reception_queue = Queue(maxsize=MAX_EVENT_RECEPTION_NUMS)
    s_player_event_reception = True
    s_enemy_event_reception = True
    s_environment_event_reception = True
    """other"""
    s_player_event_controler = None
    s_enemy_event_controler = None
    s_environment_event_controler = None
    """game"""
    s_game_running = True
    """subpub"""
    s_game_pubsub_dict = {}
    def __new__(cls):
        return None

    def __init__(self):
        #banned
        pass

    @staticmethod
    def update():
        EventControler.event_quorum()
    @staticmethod
    def init():
        #EventControler.init_controler()
        EventControler.init_event_reception()
        EventControler.init_pubsub()
        EventControler.init_log()

    @staticmethod
    def init_controler():
        #banned
        """
        EventControler.s_player_event_controler = PlayerEventControler()
        EventControler.s_enemy_event_controler = EnemyEventControler()
        EventControler.s_environment_event_controler = EnvironmentEventControler()
        """

    @staticmethod
    def init_event_reception():
        """初始化事件队列"""
        pass
        #EventControler.s_event_reception_queue = Queue(maxsize=MAX_EVENT_RECEPTION_NUMS)

    @staticmethod
    def init_pubsub():
        EventControler.s_game_pubsub_dict = {}
    @staticmethod
    def init_log():
        if EventControler.s_log_event_switch == False:
            return

        EventControler.s_log_event_counter = 0
        EventControler.s_event_logger = logger.Logger("..//logs//event_log.txt",log_level=base.GAME_LOG_EVENT_LEVEL)
        """file IO"""

    @staticmethod
    def add_subscriber(event_name,callback):
        """订阅事件控制器接收到的事件，外部调用此接口，并提供具体处理的回调"""
        if event_name not in EventControler.s_game_pubsub_dict:
            EventControler.s_game_pubsub_dict[event_name] = []
        EventControler.s_game_pubsub_dict[event_name].append(callback)
        if (EventControler.s_log_event_switch == True):
            EventControler.s_event_logger.log(f"|subcribe| {event_name}:{callback}",'DEBUG',show_console=base.GAME_LOG_EVENT_SHOWCONSOLE)

    @staticmethod
    def print_subscriber():
        """打印所有消息订阅者"""
        for key in EventControler.s_game_pubsub_dict:
            v = EventControler.s_game_pubsub_dict.get(key)
            if None != v:
                for cb in v:
                    print(cb)

    @staticmethod
    def publish(event_name, *args, **kwargs):
        """发布事件,callback注意首参数为Event类"""
        if event_name in EventControler.s_game_pubsub_dict:
            for callback in EventControler.s_game_pubsub_dict[event_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"回调执行失败: {e}")
                if(EventControler.s_log_event_switch==True):
                    pass
        else:
            print(f"ERROR:{event_name}NOT in DICT")

    @staticmethod
    def log_open():
        EventControler.s_log_event_switch = True

    @staticmethod
    def log_close():
        EventControler.s_log_event_switch = False

    @staticmethod
    def event_create():
        pass

    @staticmethod
    def event_game_send(ev)->bool:
        """静态方法，游戏进行中向本事件控制器发送的唯一事件接口,在其他模块调用"""
        EventControler.s_event_reception_queue.put(ev)
        return True
    @staticmethod
    def event_sys_get():
        """静态方法，唯一的获取sys事件的接口，同时包含系统和用户的输入事件"""

        """input judge"""
        for event in pygame.event.get():
            ev = Event(event.type)
            if(event.type == TYPE_KEYUP or event.type == TYPE_KEYDOWN):
                ev.key = event.key
                ev.event_name = NAME_USER_INPUT
            else:
                ev.event_name = NAME_DEFAULT
            EventControler.event_game_send(ev)

        """continues input judge"""
        ev = Event()#将用户持续输入所检测封入事件池中
        ev.set_event_name(NAME_USER_CONTINUES_INPUT)
        ev.keys = pygame.key.get_pressed()
        EventControler.event_game_send(ev)



    @staticmethod
    def event_quorum()->bool:
        EventControler.event_sys_get()
        if(EventControler.s_status!=1):
            return False

        for _ in range(EventControler.s_event_reception_queue.qsize()):
            try:
                ev = EventControler.s_event_reception_queue.get(block=False)  # 非阻塞
                #add to log
                if(EventControler.s_log_event_switch == True):
                    EventControler.s_log_event_counter += 1
                    if(ev.event_name!=1):
                        msg = f"type={type_dict.get(ev.type,str(ev.type))},event_name={ev.event_name},player_id={ev.player_id},enemy_id={ev.enemy_id}"
                        log_info = f"[{EventControler.s_log_event_counter}]:{msg}"
                        EventControler.s_event_logger.log(log_info,show_console=base.GAME_LOG_EVENT_SHOWCONSOLE)

            except queue.Empty:
                print("except")
                return

            if(ev.event_name == NAME_USER_CONTINUES_INPUT):
                EventControler.publish(NAME_USER_CONTINUES_INPUT,ev)
            if(ev.type == QUIT):
                EventControler.publish(QUIT,ev)
            elif(ev.event_name == NAME_USER_INPUT and EventControler.s_player_event_reception==True):
                EventControler.publish(NAME_USER_INPUT,ev)
            elif(ev.type==TYPE_ENEMY and EventControler.s_enemy_event_reception==True):
                pass
            elif (ev.type == TYPE_ENVIRONMENT and EventControler.s_environment_event_reception == True):
                pass
            else:
                continue

        return True


class PlayerEventControler:



    def __init__(self):
        pass



class EnemyEventControler:

    def __init__(self):
        pass
class EnvironmentEventControler:

    game_running = True

    def __init__(self):
        pass



#costom-type
"""自定义的TYPE类型，此TYPE类型和pygame公用一个event.type,因此不推荐，这里目前只添加了TYPE_ENEMY/TYPE_ENVIRONMENT用于区别玩家、敌人、环境的事件类型,
非pygame特有的输入事件的时候，尽量不以该类型作为仲裁判断"""
TYPE_ENEMY = 600000
TYPE_ENVIRONMENT = 600001

#costom-event_name
NAME_DEFAULT = -1
NAME_USER_INPUT = 0
NAME_USER_CONTINUES_INPUT = 1

NAME_PLAYER_MOVE = 600128
NAME_PLAYER_SHOOT = 600129

#costom - event_name - enemy
NAME_ENEMY_ACT = 600512
NAME_ENEMY_DEAD = 600513

#costom - event_name - environment - collision
NAME_ENVIRONMENT_COLLISION_P_E = 601024
NAME_ENVIRONMENT_COLLISION_P_B = 601025
NAME_ENVIRONMENT_COLLISION_B_E = 601026

"""pygame给出的类型================================================================================================="""
#pygame-type
TYPE_KEYDOWN = 768
TYPE_KEYMAPCHANGED = 772
TYPE_KEYUP = 769


#pygame-key
K_0 = 48
K_1 = 49
K_2 = 50
K_3 = 51
K_4 = 52
K_5 = 53
K_6 = 54
K_7 = 55
K_8 = 56
K_9 = 57
K_a = 97

K_AC_BACK = 1073742094

K_AMPERSAND = 38
K_ASTERISK = 42
K_AT = 64
K_b = 98
K_BACKQUOTE = 96
K_BACKSLASH = 92
K_BACKSPACE = 8
K_BREAK = 1073741896
K_c = 99
K_CAPSLOCK = 1073741881
K_CARET = 94
K_CLEAR = 1073741980
K_COLON = 58
K_COMMA = 44
K_CURRENCYSUBUNIT = 1073742005
K_CURRENCYUNIT = 1073742004
K_d = 100
K_DELETE = 127
K_DOLLAR = 36
K_DOWN = 1073741905
K_e = 101
K_END = 1073741901
K_EQUALS = 61
K_ESCAPE = 27
K_EURO = 1073742004
K_EXCLAIM = 33
K_f = 102
K_F1 = 1073741882
K_F10 = 1073741891
K_F11 = 1073741892
K_F12 = 1073741893
K_F13 = 1073741928
K_F14 = 1073741929
K_F15 = 1073741930
K_F2 = 1073741883
K_F3 = 1073741884
K_F4 = 1073741885
K_F5 = 1073741886
K_F6 = 1073741887
K_F7 = 1073741888
K_F8 = 1073741889
K_F9 = 1073741890
K_g = 103
K_GREATER = 62
K_h = 104
K_HASH = 35
K_HELP = 1073741941
K_HOME = 1073741898
K_i = 105
K_INSERT = 1073741897
K_j = 106
K_k = 107
K_KP0 = 1073741922
K_KP1 = 1073741913
K_KP2 = 1073741914
K_KP3 = 1073741915
K_KP4 = 1073741916
K_KP5 = 1073741917
K_KP6 = 1073741918
K_KP7 = 1073741919
K_KP8 = 1073741920
K_KP9 = 1073741921

K_KP_0 = 1073741922
K_KP_1 = 1073741913
K_KP_2 = 1073741914
K_KP_3 = 1073741915
K_KP_4 = 1073741916
K_KP_5 = 1073741917
K_KP_6 = 1073741918
K_KP_7 = 1073741919
K_KP_8 = 1073741920
K_KP_9 = 1073741921
K_KP_DIVIDE = 1073741908
K_KP_ENTER = 1073741912
K_KP_EQUALS = 1073741927
K_KP_MINUS = 1073741910
K_KP_MULTIPLY = 1073741909
K_KP_PERIOD = 1073741923
K_KP_PLUS = 1073741911

K_l = 108
K_LALT = 1073742050
K_LCTRL = 1073742048
K_LEFT = 1073741904
K_LEFTBRACKET = 91
K_LEFTPAREN = 40
K_LESS = 60
K_LGUI = 1073742051
K_LMETA = 1073742051
K_LSHIFT = 1073742049
K_LSUPER = 1073742051
K_m = 109
K_MENU = 1073741942
K_MINUS = 45
K_MODE = 1073742081
K_n = 110
K_NUMLOCK = 1073741907
K_NUMLOCKCLEAR = 1073741907
K_o = 111
K_p = 112
K_PAGEDOWN = 1073741902
K_PAGEUP = 1073741899
K_PAUSE = 1073741896
K_PERCENT = 37
K_PERIOD = 46
K_PLUS = 43
K_POWER = 1073741926
K_PRINT = 1073741894
K_PRINTSCREEN = 1073741894
K_q = 113
K_QUESTION = 63
K_QUOTE = 39
K_QUOTEDBL = 34
K_r = 114
K_RALT = 1073742054
K_RCTRL = 1073742052
K_RETURN = 13
K_RGUI = 1073742055
K_RIGHT = 1073741903
K_RIGHTBRACKET = 93
K_RIGHTPAREN = 41
K_RMETA = 1073742055
K_RSHIFT = 1073742053
K_RSUPER = 1073742055
K_s = 115
K_SCROLLLOCK = 1073741895
K_SCROLLOCK = 1073741895
K_SEMICOLON = 59
K_SLASH = 47
K_SPACE = 32
K_SYSREQ = 1073741978
K_t = 116
K_TAB = 9
K_u = 117
K_UNDERSCORE = 95
K_UNKNOWN = 0
K_UP = 1073741906
K_v = 118
K_w = 119
K_x = 120
K_y = 121
K_z = 122


MOUSEBUTTONDOWN = 1025
MOUSEBUTTONUP = 1026
MOUSEMOTION = 1024
MOUSEWHEEL = 1027

MULTIGESTURE = 2050

NOEVENT = 0
NOFRAME = 32

NUMEVENTS = 65535

OPENGL = 2
OPENGLBLIT = 10

PREALLOC = 16777216

QUIT = 256

RENDER_DEVICE_RESET = 8193

RENDER_TARGETS_RESET = 8192

RESIZABLE = 16

RLEACCEL = 16384
RLEACCELOK = 8192

SCALED = 512

SCRAP_BMP = 'image/bmp'
SCRAP_CLIPBOARD = 0
SCRAP_PBM = 'image/pbm'
SCRAP_PPM = 'image/ppm'
SCRAP_SELECTION = 1
SCRAP_TEXT = 'text/plain'

SHOWN = 64

SRCALPHA = 65536
SRCCOLORKEY = 4096

SWSURFACE = 0

SYSTEM_CURSOR_ARROW = 0
SYSTEM_CURSOR_CROSSHAIR = 3
SYSTEM_CURSOR_HAND = 11
SYSTEM_CURSOR_IBEAM = 1
SYSTEM_CURSOR_NO = 10
SYSTEM_CURSOR_SIZEALL = 9
SYSTEM_CURSOR_SIZENESW = 6
SYSTEM_CURSOR_SIZENS = 8
SYSTEM_CURSOR_SIZENWSE = 5
SYSTEM_CURSOR_SIZEWE = 7
SYSTEM_CURSOR_WAIT = 2
SYSTEM_CURSOR_WAITARROW = 4

SYSWMEVENT = 513

TEXTEDITING = 770
TEXTINPUT = 771

TIMER_RESOLUTION = 0

USEREVENT = 32866

USEREVENT_DROPFILE = 4096

VIDEOEXPOSE = 32770
VIDEORESIZE = 32769

WINDOWCLOSE = 32787
WINDOWDISPLAYCHANGED = 32791
WINDOWENTER = 32783
WINDOWEXPOSED = 32776
WINDOWFOCUSGAINED = 32785
WINDOWFOCUSLOST = 32786
WINDOWHIDDEN = 32775
WINDOWHITTEST = 32789
WINDOWICCPROFCHANGED = 32790
WINDOWLEAVE = 32784
WINDOWMAXIMIZED = 32781
WINDOWMINIMIZED = 32780
WINDOWMOVED = 32777
WINDOWRESIZED = 32778
WINDOWRESTORED = 32782
WINDOWSHOWN = 32774
WINDOWSIZECHANGED = 32779
WINDOWTAKEFOCUS = 32788

type_dict = {
    # 键盘事件
    768: "KEYDOWN",  # pygame.KEYDOWN
    769: "KEYUP",  # pygame.KEYUP
    770: "TEXTEDITING",  # pygame.TEXTEDITING
    771: "TEXTINPUT",  # pygame.TEXTINPUT
    772: "KEYMAPCHANGED",  # pygame.KEYMAPCHANGED (Android/iOS专用)

    # 鼠标事件
    1024: "MOUSEMOTION",  # pygame.MOUSEMOTION
    1025: "MOUSEBUTTONDOWN",  # pygame.MOUSEBUTTONDOWN
    1026: "MOUSEBUTTONUP",  # pygame.MOUSEBUTTONUP

    # 窗口事件
    256: "QUIT",  # pygame.QUIT
    257: "ACTIVEEVENT",  # pygame.ACTIVEEVENT
    32768: "VIDEORESIZE",  # pygame.VIDEORESIZE
    32769: "VIDEOEXPOSE",  # pygame.VIDEOEXPOSE
    32770: "VIDEOMINIMIZE",  # pygame.VIDEOMINIMIZE (SDL2已弃用)
    32771: "WINDOWENTER",  # pygame.WINDOWENTER
    32772: "WINDOWLEAVE",  # pygame.WINDOWLEAVE
    32773: "WINDOWFOCUSGAINED",  # pygame.WINDOWFOCUSGAINED
    32774: "WINDOWFOCUSLOST",  # pygame.WINDOWFOCUSLOST
    32775: "WINDOWCLOSE",  # pygame.WINDOWCLOSE (SDL2新增)

    # 游戏控制器事件
    1536: "JOYAXISMOTION",  # pygame.JOYAXISMOTION
    1537: "JOYBALLMOTION",  # pygame.JOYBALLMOTION
    1538: "JOYHATMOTION",  # pygame.JOYHATMOTION
    1539: "JOYBUTTONDOWN",  # pygame.JOYBUTTONDOWN
    1540: "JOYBUTTONUP",  # pygame.JOYBUTTONUP
    1541: "JOYDEVICEADDED",  # pygame.JOYDEVICEADDED
    1542: "JOYDEVICEREMOVED",  # pygame.JOYDEVICEREMOVED

    # 触摸事件 (移动设备)
    1792: "FINGERDOWN",  # pygame.FINGERDOWN
    1793: "FINGERUP",  # pygame.FINGERUP
    1794: "FINGERMOTION",  # pygame.FINGERMOTION

    # 用户自定义事件 (1024-32767)
    #1024: "USEREVENT",  # pygame.USEREVENT (基准值)
    #16383: "NUMEVENTS"  # pygame.NUMEVENTS (最大值)
}