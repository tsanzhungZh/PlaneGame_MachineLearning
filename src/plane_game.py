import pygame
import random
import sys
from event import *

if __name__ == "__main__":

    # 初始化
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("太空射击")
    clock = pygame.time.Clock()

    # 颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


    # 玩家
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 40))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = screen_width // 2
            self.rect.bottom = screen_height - 10
            self.speed = 8

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += self.speed

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


    # 敌人
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > screen_height:
                self.rect.x = random.randrange(screen_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 4)


    # 子弹
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((5, 10))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()


    # 创建精灵组
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # 生成敌人
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 游戏变量
    score = 0
    font = pygame.font.Font(None, 36)

    # 游戏主循环
    game_running = True
    while game_running:
        # 保持循环以正确的速度运行
        clock.tick(60)


        # 处理输入事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # 更新
        all_sprites.update()

        # 检查子弹是否击中敌人
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # 检查敌人是否撞到玩家
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            running = False

        # 渲染
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # 显示分数
        score_text = font.render(f"得分: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 刷新屏幕
        pygame.display.flip()

    pygame.quit()
    sys.exit()