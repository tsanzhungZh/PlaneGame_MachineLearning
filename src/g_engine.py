import pygame
import random
import sys
import base
from event import *



class G_Engine:

    s_all_sprites_group = pygame.sprite.Group()
    s_all_enemies_group = pygame.sprite.Group()
    s_running_status = base.GAME_STAUTS_RUNNING

    """pygame_setting"""
    s_screen_width = 800
    s_screen_height = 600
    s_caption = "plane game"

    def __new__(cls):
        return None

    """
    ========================= ENGINE  ==============================
    """
    @staticmethod
    def run_():

        pygame.init()
        screen = pygame.display.set_mode((G_Engine.s_screen_width, G_Engine.s_screen_height))
        pygame.display.set_caption(G_Engine.s_caption)
        clock = pygame.time.Clock()

        while(G_Engine.s_running_status == base.GAME_STAUTS_RUNNING):
            pass
        pass




    """
    ========================= PUBSUB-CALL BACK  ==============================
    """
    @staticmethod
    def init_event_cb():
        """在这里添加所有的事件订阅回调,也可以在其他模块动态添加订阅"""
        EventControler.add_subscriber(QUIT,G_Engine.cb_game_close)

    @staticmethod
    def cb_game_close(ev: Event):
        if(ev.type == QUIT):
            G_Engine.s_running_status = base.GAME_STATUS_CLOSE






# 使用示例
pubsub = PubSub()

# 订阅者
def on_message_received(message):
    print(f"收到消息: {message}")

pubsub.subscribe("message", on_message_received)

# 发布者
pubsub.publish("message", "Hello, PubSub!")  # 输出: 收到消息: Hello, PubSub!