import pygame
import random
import sys
from event import *
import torch
import AI.ai
from AI.ai import *
import g_engine
def train():
   env = g_engine.G_Engine()
   state_size = len(env._get_state())  # 取决于_get_state的实现
   action_size = 5  # 上 下 左 右 射击

   agent = DQNAgent(state_size, action_size)
   episodes = 1000
   batch_size = 32

   for e in range(episodes):
      state = env.reset()
      total_reward = 0

      while True:
         # env.render()  # 训练时可以注释掉以加快速度

         action = agent.act(state)
         next_state, reward, done = env.step(action)

         agent.remember(state, action, reward, next_state, done)
         state = next_state
         total_reward += reward

         if done:
            print(f"Episode: {e}/{episodes}, Score: {env.score}, Epsilon: {agent.epsilon:.2f}")
            break

         if len(agent.memory) > batch_size:
            agent.replay(batch_size)

   # 保存模型
   torch.save(agent.model.state_dict(), "plane_dqn.pth")








if __name__ == "__main__":
   pass