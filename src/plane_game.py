import pygame
import random
import os
import torch
import AI.ai
from AI.ai import *
from g_engine import *
from event import *
from entity import *

def train():




   """================ py game ================"""
   pygame.init()
   if (base.GAME_SHOW_SCREEN == True):
      screen = pygame.display.set_mode((G_Engine.s_screen_width, G_Engine.s_screen_height))
      pygame.display.set_caption(G_Engine.s_caption)
   clock = pygame.time.Clock()

   font = pygame.font.Font(None, 36)
   score = 0
   """================ py game ================"""


   """===================costom game content==================="""
   # costom - init moduler
   EventControler.init()
   EntityControler.init()
   # costom - add callback
   G_Engine.init_event_cb()
   # costom - add entity
   EntityControler.add_new_player(base.GAME_SCREEN_WIDTH / 2 - base.PLAYER_BODYSIZE_X / 2,
                                  base.GAME_SCREEN_HEIGHT - 2 * base.PLAYER_BODYSIZE_Y)
   # EntityControler.modify_player_attribute(attribute={'velocity_x': 40, 'velocity_y': 15,'allow_exceed_max_speed': True})
   EntityControler.add_new_bullet(base.GAME_SCREEN_WIDTH / 2 - base.BULLET_BODYSIZE_X / 2,
                                  base.GAME_SCREEN_HEIGHT - 2 * base.PLAYER_BODYSIZE_Y, base.BULLET_INITIAL_SPEED)
   EntityControler.add_new_enemy(100, 200)
   EntityControler.add_new_enemy(200, 300)
   """===================costom game content==================="""

   state_size = len(G_Engine._get_state())  # 取决于_get_state的实现
   action_size = 5  # 上 下 左 右 射击

   agent = DQNAgent(state_size, action_size)
   episodes = 1000
   batch_size = 32


   if os.path.exists("..//model//"+base.MODEL_SAVE_NAME):
      agent.model.load_state_dict(torch.load("..//model//"+base.MODEL_SAVE_NAME))
      agent.epsilon = max(agent.epsilon_min, agent.epsilon * 0.8)  # 从较低探索率开始
      print("Loaded existing model")
   else:
      print("Starting new training")


   it_cnt = 0

   for e in range(episodes):
      print("new episode")
      state = G_Engine.reset()
      total_reward = 0

      while True:

         if(base.GAME_SHOW_SCREEN == True):# 训练时可以False掉以加快速度
            G_Engine.render(screen)
            clock.tick(120)

         action = agent.act(state)
         next_state, reward, done = G_Engine.step(action)

         agent.remember(state, action, reward, next_state, done)
         state = next_state
         total_reward += reward


         it_cnt += 1
         if (it_cnt > 10000):
            it_cnt = 0
            torch.save(agent.model.state_dict(), '..//model//dqn_model.pth')
            print("saving model at ..//model//dqn_model.pth")

         if not done:
            print(f"Episode: {e}/{episodes}, Score: {score}, Epsilon: {agent.epsilon:.2f}")
            break

         if len(agent.memory) > batch_size:
            agent.replay(batch_size)



   # 保存模型
   torch.save(agent.model.state_dict(), '..//model//dqn_model.pth')



if __name__ == "__main__":
   train()