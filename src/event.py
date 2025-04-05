
class Event:
    """"""
    type = 0
    priority = 0xff
    # 类属性（所有实例共享）
    id = 0

    # 初始化方法（构造函数）
    def __init__(self,type,priority = 0xff):
        self.type = type  # 实例属性
        self.priority = priority



class EventControler:
    """key range :(1,10000),used for event log """
    s_log_event_counter = 0
    s_log_event_hash = {}
    s_log_event_switch = False
    """0关闭 1空闲中 2处理中    """
    s_status = 1


    def __init__(self):
        #self.s_log_event_hash.clear()
        #self.s_status = 1
        pass
    @staticmethod
    def log_open():
        EventControler.s_log_event_switch = True

    @staticmethod
    def log_close():
        EventControler.s_log_event_switch = False

    @staticmethod
    def event_id_alloc(type,priority = 0xff) -> Event:
        ret = Event(type,priority)
        if(EventControler.log_event_switch == True):
            ret.id = EventControler.log_event_counter+1
            EventControler.log_event_counter += 1
        else:
            ret.id = 0

        return ret


