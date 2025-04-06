import pygame
import random
import sys
from event import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()


    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.radius = 20
            self.color = (0, 100, 255)

            # 运动参数
            self.velocity_x = 0
            self.velocity_y = 0
            self.acceleration = 0.5  # 加速度
            self.max_speed = 5  # 最大速度
            self.friction = 0.95  # 摩擦系数(0-1)

        def update(self, keys):
            # 加速度计算
            if keys[pygame.K_LEFT]:
                self.velocity_x -= self.acceleration
            if keys[pygame.K_RIGHT]:
                self.velocity_x += self.acceleration
            if keys[pygame.K_UP]:
                self.velocity_y -= self.acceleration
            if keys[pygame.K_DOWN]:
                self.velocity_y += self.acceleration

            # 限制最大速度
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
            self.x = max(self.radius, min(self.x, 800 - self.radius))
            self.y = max(self.radius, min(self.y, 600 - self.radius))

        def draw(self, surface):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


    player = Player(400, 300)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill((0, 0, 0))
        player.draw(screen)

        # 显示速度信息
        font = pygame.font.SysFont(None, 24)
        speed_text = font.render(f"速度: ({player.velocity_x:.1f}, {player.velocity_y:.1f})", True, (255, 255, 255))
        screen.blit(speed_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)