# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random
import copy
import math

#b键：开始
#s键：暂停
#0~9数字键：生成存活率为 0% ~ 9% 的随机世界（暂停状态）
#鼠标点击：改变当前细胞状态（暂停状态）

####################################################################
#一个改变细胞控制矩阵的函数
#左上角开始，第一个细胞为(0,0)，state=1为活，state=0为死
def change_matrix(x,y,state):
    GameLifeMatrix[y+1][x+1]=state
####################################################################

####################################################################
#查看细胞状态的函数
#左上角开始，第一个细胞为(0,0)，state=1为活，state=0为死
def visit_matrix(x,y):
    return GameLifeMatrix[y+1][x+1]
####################################################################

####################################################################
#一个绘制细胞活或死的函数
# 左上角开始，第一个细胞为(0,0)，state=1为活，state=0为死
def draw_cell(x,y,state):
    if state==1:
        pygame.draw.rect(screen, \
                         cell_life_color, \
                         Rect(x_begin+x*length+1, \
                              y_begin+y*Wide+1,length-2,Wide-2))
    else:
        pygame.draw.rect(screen, \
                         cell_died_color, \
                         Rect(x_begin+x*length+1, \
                              y_begin+y*Wide+1,length-2,Wide-2))
####################################################################

####################################################################
#改变细胞存在状态的函数，同时改变矩阵和图像
# 左上角开始，第一个细胞为(0,0)，state=1为活，state=0为死
def change_cell(x,y,state):
    change_matrix(x,y,state)
    draw_cell(x,y,state)
####################################################################

####################################################################
#根据给出的存活率，生成一个随机世界状态
def random_generate(NumL,NumW,propert_life):
    for x in range(0,NumL):
        for y in range(0,NumW):
            change_cell(x,y,0)
    NumCellLife=int(NumL*NumW*propert_life)
    for n in range(0,NumCellLife):
        x=random.randint(0,NumL-1)
        y=random.randint(0,NumW-1)
        change_cell(x,y,1)
####################################################################

####################################################################
#世界开始运行的函数
def Run():
    #规则：
    #1. 周围有三个活细胞，此细胞为活
    #2. 周围有两个活细胞，此细胞不变
    #3. 否则，此细胞死
    x_add=[-1, 0, 1, 1, 1, 0, -1, -1]
    y_add=[-1, -1, -1, 0, 1, 1, 1, 0]
    for x in range(0,NumL):
        for y in range(0,NumW):
            Sum=0
            for i in range(0,len(x_add)):
                Sum=Sum+visit_matrix(x+x_add[i],y+y_add[i])
            if Sum==3:
                change_cell(x,y,1)
            elif Sum==2:
                pass
            else:
                change_cell(x,y,0)
    #显示年限
    if Year==1 or Year==0:
        text_when_running[1]="After "+str(Year)+" year..."
    elif Year<=999:
        text_when_running[1]="After "+str(Year)+" years..."
    else:
        text_when_running[1]="After many many years... (Please stop it.)"
    if have_warning==1:
        text_when_running[2]=warning_text_when_run[1]
    else:
        text_when_running[2]=''
    display_text(text_when_running)
####################################################################

####################################################################
#三行字显示的函数
def display_text(text):
    #清空区域
    pygame.draw.rect(screen,(255,255,255),Rect(0,0,ScreenSize[0],3*text_surface.get_height()+10))
    #显示字
    for n in range(0,3):
        text_to_display=font.render(text[n],True,(0,0,0))
        screen.blit(text_to_display,(math.fabs(ScreenSize[0]/2-6*len(text[n])/2),text_surface.get_height()/2+text_surface.get_height()*n))
#####################################################################

text_when_wait=["Press 'b' to start the game.",\
                "Press number to change the property of life",\
                "Now, let's begin the game!!"]
warning_text_when_run=["",\
                       "Please Stop First!!!",\
                       ""]
text_when_running=["",\
                   "",\
                   ""]
text_when_peace=["Now, world is in the peace ~~~~~~~", \
                 "Press 'b' to start the game.", \
                 "Press number to change the property of life"]
text_when_zero=["Now, all life has been died!!!", \
                "Press 'b' to start the game.", \
                "Press number to change the property of life"]
pygame.init()
ScreenSize=(640,480)
screen=pygame.display.set_mode(ScreenSize,0,32)
screen.fill((255,255,255))
font=pygame.font.SysFont("menlo",20)
text_surface=font.render(text_when_running[1],True,(0,0,0))
display_text(text_when_wait)
#定义细胞颜色
cell_died_color=(255,255,255)#死亡-》白色
cell_life_color=(255,0,0)#活-》红色
#定义细胞横竖个数
NumL=50
NumW=50
#定义左上角第一个细胞的左上角像素点
x_begin=15
y_begin=10+3*text_surface.get_height()
#计算一个细胞的长宽
length=int((ScreenSize[0]-2*x_begin)/NumL)
Wide=int((ScreenSize[1]-2*y_begin+3*text_surface.get_height())/NumW)
#画出整个map
for x in range(0,NumL):
    for y in range(0,NumW):
        pygame.draw.rect(screen,(0,0,0),\
                         Rect((x_begin+x*length,y_begin+y*Wide),\
                              (length,Wide)),1)
#生成细胞控制矩阵
GameLifeMatrix=[]
for y in range(0,NumW+2):
    GameLifeMatrixRow=[]
    for x in range(0,NumL+2):
        GameLifeMatrixRow.append(0)
    GameLifeMatrix.append(GameLifeMatrixRow)
GameLifeMatrixZero=copy.deepcopy(GameLifeMatrix)#复制一个全0矩阵为后面判断做准备
#生成一个存活率为50%的世界
random_generate(NumL,NumW,0.1)

#变量 Run State 为了控制游戏是否在进行
RunState=0
#记录年限
Year=0
#warning提示flag
have_warning=0
#开始循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT: #按关闭按钮就退出
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key==K_b: #b键开始
                RunState=1
            elif event.key==K_s: #s键暂停，年限不归零
                have_warning=0
                RunState=0
                display_text(text_when_wait)
            # 数字键产生随机生命（暂停状态，年限归零）
            elif event.key==K_0:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0)
                    Year=0
                else:
                    have_warning=1
            elif event.key==K_1:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.1)
                else:
                    have_warning=1
            elif event.key==K_2:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.2)
                else:
                    have_warning=1
            elif event.key==K_3:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.3)
                else:
                    have_warning=1
            elif event.key==K_4:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.4)
                else:
                    have_warning=1
            elif event.key==K_5:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.5)
                else:
                    have_warning=1
            elif event.key==K_6:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.6)
                else:
                    have_warning=1
            elif event.key==K_7:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.7)
                else:
                    have_warning=1
            elif event.key==K_8:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.8)
                else:
                    have_warning=1
            elif event.key==K_9:
                if RunState==0:
                    Year=0
                    random_generate(NumL,NumW,0.9)
                else:
                    have_warning=1
        elif event.type==MOUSEBUTTONDOWN:
            if RunState==0:
                #返回鼠标点击的细胞坐标，左上角开始，第一个为(0,0)
                ClickX=int((event.pos[0]-x_begin)/length)
                ClickY=((event.pos[1]-y_begin)/Wide)
                #改变点击位置细胞状态
                if visit_matrix(ClickX,ClickY):
                    change_cell(ClickX,ClickY,0)
                else:
                    change_cell(ClickX,ClickY,1)
            else:
                have_warning=1
    if RunState==1:
        GameLifeMatrix_copy=copy.deepcopy(GameLifeMatrix) # copy一个matrix，为了验证是否进化已经停止
        Run()
        Year=Year+1
        if GameLifeMatrix==GameLifeMatrix_copy: # 如果进化停止，结束游戏
            RunState=0
            Year=0
            have_warning=0
            display_text(text_when_peace)
        elif GameLifeMatrix==GameLifeMatrixZero: # 如果全部死亡，结束游戏
            RunState=0
            Year=0
            have_warning=0
            display_text(text_when_zero)
    else:
        pass
    pygame.display.update()
