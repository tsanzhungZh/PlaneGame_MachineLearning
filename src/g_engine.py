import pygame
import random
import sys
import base
from event import *
from entity import *


class G_Engine:

    s_running_status = base.GAME_STAUTS_RUNNING

    """pygame_setting"""
    s_screen_width = base.GAME_SCREEN_WIDTH
    s_screen_height = base.GAME_SCREEN_HEIGHT
    s_caption = "plane game"

    def __new__(cls):
        return None

    """
    ========================= ENGINE  ==============================
    """
    @staticmethod
    def run():
        #pygame
        pygame.init()
        screen = pygame.display.set_mode((G_Engine.s_screen_width, G_Engine.s_screen_height))
        pygame.display.set_caption(G_Engine.s_caption)
        clock = pygame.time.Clock()

        font = pygame.font.Font(None, 36)
        score = 0

        #costom - init moduler
        EventControler.init()
        EntityControler.init()

        #costom - add callback
        G_Engine.init_event_cb()

        #costom - add entity
        player = Player()
        EntityControler.add_new_player(player)



        while(G_Engine.s_running_status == base.GAME_STAUTS_RUNNING):

            clock.tick(60)

            #ev = Event()
            #EventControler.event_game_send(ev)

            EventControler.update()
            EntityControler.update()


            # 渲染
            screen.fill(base.BLACK)
            EntityControler.draw(screen)

            # 显示分数
            score_text = font.render(f"得分: {score}", True, base.WHITE)
            screen.blit(score_text, (10, 10))

            # 刷新屏幕
            pygame.display.flip()

        pygame.quit()
        sys.exit()



    """
    ========================= PUBSUB-CALL BACK  ==============================
    """
    @staticmethod
    def init_event_cb():
        """在这里添加所有的事件订阅回调,也可以在其他模块动态添加订阅"""
        EventControler.add_subscriber(QUIT,G_Engine.cb_game_close)
        print(QUIT)
    @staticmethod
    def cb_game_close(ev: event.Event)->None:
        print("close")
        if(ev.type == QUIT):
            G_Engine.s_running_status = base.GAME_STATUS_CLOSE







G_Engine.run()

