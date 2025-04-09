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
    def reset():
        """重置游戏状态"""
        """
        EntityControler.
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        return self._get_state()
        """
        EntityControler.reset()
        return G_Engine._get_state()

    @staticmethod
    def run():
        #pygame
        pygame.init()
        if(base.GAME_SHOW_SCREEN == True):
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
        EntityControler.add_new_player(base.GAME_SCREEN_WIDTH/2 - base.PLAYER_BODYSIZE_X/2,base.GAME_SCREEN_HEIGHT - 2 * base.PLAYER_BODYSIZE_Y)
        #EntityControler.modify_player_attribute(attribute={'velocity_x': 40, 'velocity_y': 15,'allow_exceed_max_speed': True})
        EntityControler.add_new_bullet(base.GAME_SCREEN_WIDTH/2 - base.BULLET_BODYSIZE_X/2,base.GAME_SCREEN_HEIGHT - 2 * base.PLAYER_BODYSIZE_Y,base.BULLET_INITIAL_SPEED)

        EntityControler.add_new_enemy(100,200)
        EntityControler.add_new_enemy(200,300)

        while(G_Engine.s_running_status == base.GAME_STAUTS_RUNNING):



            G_Engine.step()
            #costom
            #EntityControler.set_player_pos(100,200)
            enemy = EntityControler.get_closest_enemy_around_player()
            if(enemy!=None):
                pass

            #screen show
            if(base.GAME_SHOW_SCREEN == True):
                G_Engine.render(screen)
                clock.tick(60)


        pygame.quit()
        sys.exit()

    @staticmethod
    def render(screen):

        if(screen == None):
            return

        # 渲染
        screen.fill(base.BLACK)
        EntityControler.draw(screen)
        # 显示分数
        #score_text = font.render(f"得分: {score}", True, base.WHITE)
        #screen.blit(score_text, (10, 10))
        # 刷新屏幕
        pygame.display.flip()

    @staticmethod
    def _get_state()->list:

        enemy_x = 0
        enemy_y = 0
        be = EntityControler.is_exist_bullets()
        bullet_exist = 1 if be else 0

        enemy_id = EntityControler.get_closest_enemy_around_player()
        enemy = EntityControler._get_entity(enemy_id)
        if(enemy != None):
            enemy_x = enemy.x / base.GAME_SCREEN_WIDTH
            enemy_y = enemy.y / base.GAME_SCREEN_HEIGHT

        player = EntityControler.get_player()

        player_x = player.x / base.GAME_SCREEN_WIDTH
        player_y = player.y / base.GAME_SCREEN_HEIGHT

        return [player_x,player_y,enemy_x,enemy_y,bullet_exist]

    @staticmethod
    def step(action=5):

        # 执行动作: 0-上移, 1-下移, 2-左, 3-右 ,4-射击 (5 nothing)
        EntityControler.set_player_action(action)

        state = G_Engine._get_state()
        # update
        EventControler.update()
        EntityControler.update()

        if EntityControler.g_player_survive == False:
            reward = -10
        else:
            reward = 0.1# 存活奖励

        if (action == 4):
            reward = -0.1


        return state, reward, EntityControler.g_player_survive






    """
    ========================= PUBSUB-CALL BACK  ==============================
    """
    @staticmethod
    def init_event_cb():
        """在这里添加所有的事件订阅回调,也可以在其他模块动态添加订阅"""
        EventControler.add_subscriber(QUIT,G_Engine.cb_game_close)
    @staticmethod
    def cb_game_close(ev: event.Event)->None:
        print("close")
        if(ev.type == QUIT):
            G_Engine.s_running_status = base.GAME_STATUS_CLOSE
