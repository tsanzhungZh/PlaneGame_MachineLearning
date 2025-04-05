import pygame
import random
import sys

class Event:
    """"""
    type = 0
    priority = 0xff
    # 类属性（所有实例共享）
    id = 0

    # 初始化方法（构造函数）
    def __init__(self,e_type,priority = 0xff):
        self.type = e_type  # 实例属性
        self.priority = priority
        self.id = 0

    def __del__(self):
        pass






class EventControler:
    """key range :(1,10000),used for event log """
    s_log_event_counter = 0
    s_log_event_hash = {}
    s_log_event_switch = False
    """0关闭 1空闲中 2处理中    """
    s_status = 1
    """moduler reception"""
    s_player_event_receptioin = True
    s_enemy_event_receptioin = True
    s_environment_event_receptioin = True


    def __init__(self):
        #self.s_log_event_hash.clear()
        #self.s_status = 1
        pass

    @staticmethod
    def Create():
        pass


    @staticmethod
    def log_open():
        EventControler.s_log_event_switch = True

    @staticmethod
    def log_close():
        EventControler.s_log_event_switch = False

    @staticmethod
    def event_create(e_type,priority = 0xff) -> Event:
        ret = Event(e_type,priority)
        if(EventControler.s_log_event_switch == True):
            ret.id = EventControler.s_log_event_counter+1
            EventControler.s_log_event_counter += 1
        else:
            ret.id = 0

        return ret

    @staticmethod
    def event_quorum(ev)->bool:
        if(EventControler.s_status!=1):
            return False

        if(ev.type==0 and EventControler.s_player_event_receptioin==True):
            """player"""
            pass
        elif(ev.type==1 and EventControler.s_enemy_event_receptioin==True):
            """enemy"""
            pass
        elif(ev.type==2 and EventControler.s_environment_event_receptioin==True):
            """environment"""
            pass
        else:
            return False

        return True


class PlayerEventControler:

    def __init__(self):
        pass


