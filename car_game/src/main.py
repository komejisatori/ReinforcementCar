import pygame
import sys
from pygame.locals import *

import config.resource as RESOURCE
import config.game as GAME_SETTING


def main():
    print('welcome to car game')

    # 初始化pygame
    pygame.init()

    size = width, height = GAME_SETTING.GAME_SCREEN_WIDTH, GAME_SETTING.GAME_SCREEN_HEIGHT
    speed = [-2, 1]

    # 背景设置，全白
    img_bg = pygame.image.load(RESOURCE.IMAGE_COVER_FILE_PATH)
    color_bg = (255, 255, 255)

    # 创建指定大小的窗口 Surface对象
    screen = pygame.display.set_mode(size)
    # 设置窗口标题
    pygame.display.set_caption(GAME_SETTING.GAME_TITLE)
    img_icon = pygame.image.load(RESOURCE.IMAGE_ICON_FILE_PATH)
    pygame.display.set_icon(img_icon)

    img_car = pygame.image.load(RESOURCE.IMAGE_CAR_FILE_PATH)
    img_car = pygame.transform.scale(img_car, (GAME_SETTING.GAME_CAR_WIDTH, GAME_SETTING.GAME_CAR_HEIGHT))

    # 获得图像的位置矩形
    position = img_car.get_rect()


    # Main Loop
    speed = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == KEYDOWN:

                if event.key == K_LEFT:
                    print(f'[event] left key pushed.')
                    speed = [-2, 0]

                if event.key == K_RIGHT:
                    print(f'[event] right key pushed.')
                    speed = [2, 0]

                if event.key == K_UP:
                    print(f'[event] up key pushed.')
                    speed = [0, -2]

                if event.key == K_DOWN:
                    print(f'[event] down key pushed.')
                    speed = [0, 2]

        # TODO: move the object
        position = position.move(speed)

        # fill bg
        screen.fill(color_bg)
        # 更新图像
        screen.blit(img_car, position)
        # 更新界面
        pygame.display.flip()
        # 延时
        pygame.time.delay(50)


if __name__ == "__main__":
    main()
