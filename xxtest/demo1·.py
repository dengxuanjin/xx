from random import random

import pygame

pygame.init()
screen = pygame.display.set_mode((1400, 700))  # 设置画布宽度
pygame.display.set_caption('pygame第一次测试')  # 设置画布标题

img = pygame.image.load('../../img/baox1.png').convert()
while_bol = True  # 设置循环标记

x = 100
y = 100
img2 = screen.blit(img, (x, y))
screen_width = 1400
screen_height = 700


class Player(pygame.sprite.Sprite):
    """
    player对象
    """

    def __init__(self, health, width, flag, *groups):
        super().__init__(*groups)
        self.image_text = ''
        self.image = pygame.image.load('./image/player.gif').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (health, width)
        self.vel_y = 0
        self.jumped = False
        self.flag = flag

    def set_img(self, img):
        self.image_text = img

    def update(self):
        x_move = 0
        y_move = 0

        # 获取按键，并进行相应的移动
        key = pygame.key.get_pressed()

        if self.flag:

            if key[pygame.K_UP] and self.jumped is False:
                self.vel_y = -18
                self.jumped = True

            if not key[pygame.K_UP]:
                self.jumped = False

            if key[pygame.K_LEFT]:
                x_move -= 10

            if key[pygame.K_RIGHT]:
                x_move += 10
        else:
            if key[pygame.K_w] and self.jumped is False:
                self.vel_y = -18
                self.jumped = True

            if not key[pygame.K_w]:
                self.jumped = False

            if key[pygame.K_a]:
                x_move -= 10

            if key[pygame.K_d]:
                x_move += 10

        # 添加角色重力（跳跃之后自然下落）
        self.vel_y += 1.2
        if self.vel_y > 10:
            self.vel_y = 10

        y_move += self.vel_y
        self.rect.x += x_move
        self.rect.y += y_move

        # 控制人物的最低位置

        if self.rect.bottom > screen_height - 130:
            self.rect.bottom = screen_height - 130

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # 绘制人物
        screen.blit(self.image, self.rect)


class star(pygame.sprite.Sprite):
    def __init__(self, img, *groups):
        super().__init__(*groups)
        self.image_text = img
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.midtop = (int(random() * 1400) + 1, 0)
        self.vel_y = 0

    def update(self) -> None:
        # x_move = 0
        y_move = 0
        self.vel_y += 0.1

        y_move += self.vel_y
        if self.rect.y > 700:
            self.rect.midtop = (int(random() * 1400) + 1, 0)
            self.vel_y = 0
        # self.rect.x += x_move
        self.rect.y += y_move

        screen.blit(self.image, self.rect)


class Label(pygame.sprite.Sprite):
    font_path = 'C:\\Windows\\Fonts\\simfang.ttf'

    def __init__(self, text, size, color, *groups):
        super().__init__(*groups)
        self.font = pygame.font.Font(self.font_path, size)
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def update(self) -> None:
        screen.blit(self.image, (0, 0))


bg = pygame.image.load('../../img/10.jpg')
player = Player(700, screen_height - 130, True)
# player2 = Player(100, screen_height - 130, False)     # 玩家2
clock = pygame.time.Clock()  # 设置时钟
score_label = Label("玩家 1 : %d" % 0, 32, (0, 0, 255))
st = pygame.sprite.Group()
pl = pygame.sprite.Group(player)
tx = pygame.sprite.Group()
CREATE_ENEMY_EVENT = pygame.USEREVENT

pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)

sum = 0
while while_bol:
    clock.tick(80)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():  # 获取当前所有的事件
        if event.type == pygame.QUIT:  # 与自带的退出标识作比较
            while_bol = False  # 修改循环标记
        elif event.type == CREATE_ENEMY_EVENT:
            xx = ['xx1', 'xx2', 'xx3', 'xx4']
            s = star(f'./image/{xx[int(random() * 3)]}.png')
            st.add(s)

    gc = pygame.sprite.groupcollide(st, pl, True, False)

    if gc:
        for i in gc:
            if i.image_text == './image/xx2.png':
                sum += 1
            elif i.image_text == './image/xx3.png':
                sum += 2
            elif i.image_text == './image/xx1.png':
                sum += 3
            elif i.image_text == './image/xx4.png':
                sum += 4
        score_label.set_text('paler 1 :' + str(sum))

    score_label.update()
    st.draw(screen)
    # pygame.draw.circle(screen, (255, 0, 0), (40, 40), 40)  # 自带的画圆方法\
    st.update()
    st.draw(screen)
    pl.update()
    pl.draw(screen)
    pygame.display.update()  # 更新画布
pygame.quit()
