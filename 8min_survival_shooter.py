import math
import random
from tkinter import messagebox
import os
import pygame
import pygame as pg
import cv2


cap1=cv2.VideoCapture('./temp/game_part1.mp4')
cap2=cv2.VideoCapture('./temp/game_part2.mp4')
cap3=cv2.VideoCapture('./temp/gameend.mp4')
cap4=cv2.VideoCapture('./temp/win.mp4')
print(pygame.version)
vec = pg.math.Vector2
pygame.mixer.init()
pygame.init()

path= os. getcwd()


w=1890
h=1080
fps=60
damage1=pygame.image.load("./temp/BloodOverlay-min.png")
damage1=pygame.transform.scale(damage1,(w,h))
damage2=pygame.image.load("./temp/damage2-min.png")
damage2=pygame.transform.scale(damage2,(w,h))
heart=pygame.image.load('./temp/heart (1).png')

heart=pygame.transform.scale(heart,[50,50])
ammo1=pygame.image.load('./temp/ammo/2ammo.png')
ammo1=pygame.transform.scale(ammo1,[50,50])

sammo=pygame.image.load("./temp/ammo/shotgunammo.png")
sammo=pygame.transform.scale(sammo,[50,50])
deadimg=pygame.image.load('./temp/dead_Sprite/tile005.png')
win=pygame.display.set_mode((w,h))
background=pygame.image.load("./temp/pzmap-min.png")
background=pygame.transform.scale(background,(w,h))
backrect=background.get_rect()
####################3hopper
hopperj=[]
os.chdir('./temp/jumper')
for x in os.listdir():
    image=pygame.image.load(x)
    image=pygame.transform.scale(image,(80,80))
    hopperj.append(image)
os.chdir(path)

simg = []
os.chdir('./temp/dead_Sprite')
for x in os.listdir():
    img = pygame.image.load(x)
    simg.append(img)
os.chdir(path)

head=[]
os.chdir('./temp/head')
for x in os.listdir():
    image=pygame.image.load(x)
    image=pygame.transform.scale(image,(130,130))
    head.append(image)
os.chdir(path)
######################################## zombie
zombiewalk=[]
os.chdir('./temp/zombie/walk')
for x in os.listdir():
    img=pygame.image.load(x)
    img=pygame.transform.scale(img,(80,80))
    img=pygame.transform.rotate(img,270)
    zombiewalk.append(img)
os.chdir(path)
zombieattack=[]
os.chdir('./temp/zombie/attack')
for x in os.listdir():
    img=pygame.image.load(x)
    img=pygame.transform.scale(img,(80,80))
    zombieattack.append(img)

os.chdir(path)
bosswalk=[]
os.chdir('./temp/bob')
for x in os.listdir():
    img = pygame.image.load(x)
    img = pygame.transform.scale(img, (150,150))
    img = pygame.transform.rotate(img, 270)
    bosswalk.append(img)

os.chdir(path)
dead=[]

img0=pygame.image.load("./temp/p1 (2).png")
img0=pygame.transform.scale(img0,[80,80])
img0=pygame.transform.rotate(img0,270)

img1=pygame.image.load("./temp/p1 (1)-min.png")
img1=pygame.transform.scale(img1,[80,80])
img1=pygame.transform.rotate(img1,270)

img2=pygame.image.load("./temp/p1 (3).png")
img2=pygame.transform.scale(img2,[80,80])
img2=pygame.transform.rotate(img2,270)

output_string=''
pistol='./temp/ammo/0gunt.png'

machinegun='./temp/ammo/1gunt.png'


class player():
    def __init__(self):
        self.posx=200
        self.posy=200
        self.original_image=img0
        self.speed=3
       # self.gun=0
        self.health=100*fps
        self.rect=self.original_image.get_rect()
        self.rect.x=self.posx
        self.rect.y=self.posy
        self.player_pos = pygame.Vector2(w // 3, h // 3)
        self.gun=0
        self.gun0=[10,500]
        self.gun1=[10,200]
        self.gun2=[10,20]
        self.currenthead=head[5]

    def ml(self):
        if self.posx>220:self.posx-=self.speed
        #pygame.mixer.Sound('D:\\pyprogs\\stimulation\\temp\\sounds\\grass.mp3').play()
    def mr(self):
        if self.posx<w-220:self.posx+=self.speed
        #pygame.mixer.Sound('D:\\pyprogs\\stimulation\\temp\\sounds\\grass.mp3').play()
    def mu(self):
        if self.posy>100:self.posy-=self.speed
        #pygame.mixer.Sound('D:\\pyprogs\\stimulation\\temp\\sounds\\grass.mp3').play()
    def md(self):
        if self.posy<h-210:self.posy+=self.speed
        #pygame.mixer.Sound('D:\\pyprogs\\stimulation\\temp\\sounds\\grass.mp3').play()
    def draw(self,win):
        self.rect.x = self.posx-40
        self.rect.y = self.posy-40
        mouse_x, mouse_y = pygame.mouse.get_pos()
        radians = math.atan2(mouse_y - self.posy, mouse_x - self.posx)
        self.angle = math.degrees(radians) * -1
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        win.blit(rotated_image, (self.posx - rotated_image.get_width() / 2, self.posy - rotated_image.get_height() / 2))
        pygame.draw.line(win,"red",[self.posx,self.posy],[mouse_x,mouse_y])
        #pygame.draw.rect(win, 'green', pygame.Rect(self.posx-40,self.posy-40,self.rect[2],self.rect[3]),1)
        if self.health<=50:
            self.currenthead=head[2]

class bullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 35
        self.cooldown = 500
        self.last_fired_time = 0
        x, y = pygame.mouse.get_pos()
        dx = x - self.x
        dy = y - self.y
        self.angle = math.atan2(dx, dy)
    def move(self):
        self.bul = pygame.draw.rect(win, "yellow", (self.x, self.y, 7, 5))
        current_time = pygame.time.get_ticks()
        time_since_last_fired = current_time - self.last_fired_time

        if time_since_last_fired >= self.cooldown:
            self.mvx = math.sin(self.angle) * self.speed
            self.mvy = math.cos(self.angle) * self.speed
            self.x += self.mvx
            self.y += self.mvy


class boss(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.name='boss'
        self.sprites = bosswalk
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        # self.rect.w = 10;
        self.rect.h += 15
        #self.sound = random.choice([False, False, True, False, False])
        self.drops = random.choice([False, False, False, True, False])
        self.bdrops = random.choice([False, True])
        self.sbdrops = random.choice([False, True])
        self.dropsitem = [1, 2, 3, 4, 5, 6, 7]
        self.speed_factor = 0.4
        self.rect_pos = pygame.Vector2(posx, posy)
        self.health =1400
        self.count = 0

    def deadpos(self):
        return (self.rect.x, self.rect.y)

    def update(self, target_posx, target_posy):
        try:
            # self.count += 1
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            radians = math.atan2(target_posx - self.rect.x, target_posy - self.rect.y)

            self.angle = math.degrees(radians) * -1
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -self.angle)


            target_position = pygame.Vector2(target_posx, target_posy)
            direction = target_position - self.rect_pos
            direction.normalize_ip()
            self.rect_pos += direction * self.speed_factor
            self.rect.x = self.rect_pos.x
            self.rect.y = self.rect_pos.y

            if self.health == 0:
                simg = []
                os.chdir('./temp/dead_Sprite')
                for x in os.listdir():
                    img = pygame.image.load(x)
                    simg.append(img)
                os.chdir(path)
                self.sprites = simg

                self.current_sprite += 0.2
                if self.current_sprite >= len(self.sprites):
                    self.sprites.clear()
                    del self
            else:
                self.current_sprite += 0.2
                self.count += 1
        except Exception as e:
            pass



class zombie(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.name='zombie'
        self.sprites = zombiewalk
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.sbdrops=False
        # self.rect.w = 10;
        self.rect.h += 15
        #self.sound = random.choice([False, False, True, False, False])
        self.drops = random.choice([False, False, False, False, False])
        self.bdrops = random.choice([False, False, False, False,False, False, False])
        self.dropsitem = [1, 2, 3, 4, 5, 6, 7]
        self.speed_factor = 0.8
        self.rect_pos = pygame.Vector2(posx, posy)
        self.health = 5
        self.count = 0

    def deadpos(self):
        return (self.rect.x, self.rect.y)

    def update(self, target_posx, target_posy):
        try:
            # self.count += 1
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            radians = math.atan2(target_posx - self.rect.x, target_posy - self.rect.y)

            self.angle = math.degrees(radians) * -1
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -self.angle)


            target_position = pygame.Vector2(target_posx, target_posy)
            direction = target_position - self.rect_pos
            direction.normalize_ip()
            self.rect_pos += direction * self.speed_factor
            self.rect.x = self.rect_pos.x
            self.rect.y = self.rect_pos.y
            # if self.sound==True:
            #     pygame.draw.rect(win, 'green', pygame.Rect(self.rect), 1)
            # else:
            #     pygame.draw.rect(win,'red',pygame.Rect(self.rect),1)
            # if self.count % 200 == 0:
            #     # if self.sound == True:
            #     #     pygame.mixer.Sound('D:\\pyprogs\\stimulation\\temp\\sounds\\hopperroar.mp3').play().set_volume(0.1)
            if self.health == 0:
                simg = []
                os.chdir('./temp/dead_Sprite')
                for x in os.listdir():
                    img = pygame.image.load(x)
                    simg.append(img)
                os.chdir(path)
                self.sprites = simg

                self.current_sprite += 0.2
                if self.current_sprite >= len(self.sprites):
                    self.sprites.clear()
                    del self
            else:
                self.current_sprite += 0.2
                self.count += 1
        except Exception as e:
            pass


class Hopper(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.name='hopper'
        self.sprites = hopperj
        self.current_sprite = 0
        self.sbdrops = False
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.rect.w-=10;self.rect.h-=10
        self.sound=random.choice([False,False,False,False,True,False,False])
        self.drops=random.choice([False,False,False,True,False])
        self.bdrops=random.choice([False,False,False,False,True,False,False])
        self.dropsitem=[1,2,3,4,5,6,7]
        self.speed_factor = 1
        self.rect_pos = pygame.Vector2(posx, posy)
        self.health=100
        self.count=0
    def deadpos(self):
        return (self.rect.x, self.rect.y)
    def update(self, target_posx, target_posy):
        try:
            #self.count += 1
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            radians = math.atan2(target_posx - self.rect.x, target_posy - self.rect.y)
            self.angle = math.degrees(radians) * -1
            if self.angle > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            target_position = pygame.Vector2(target_posx, target_posy)
            direction = target_position - self.rect_pos
            direction.normalize_ip()
            if self.count % 20 == 0:
                self.speed_factor = 20
            else:
                self.speed_factor = 0
            self.rect_pos += direction * self.speed_factor
            self.rect.x = self.rect_pos.x
            self.rect.y = self.rect_pos.y
            # pygame.draw.rect(win, 'red', pygame.Rect(self.rect), 1)
            if self.count%200==0:
                if self.sound==True:
                    pygame.mixer.Sound('./temp/sounds/hopperroar.mp3').play().set_volume(0.1)
            if self.health <= 0:
                simg = []
                os.chdir('./temp/dead_Sprite')
                for x in os.listdir():
                    img = pygame.image.load(x)
                    simg.append(img)
                os.chdir(path)
                self.sprites = simg
                # self.image=pygame.image.load('D:\\pyprogs\\stimulation\\temp\\dead_Sprite\\tile005.png')
                #self.count = 0
                self.current_sprite += 0.2
                if self.current_sprite >= len(self.sprites):
                    self.sprites.clear()
                    del self
            else:
                self.current_sprite += 0.2
                self.count+=1
        except Exception as e:
            pass


def ex():
    f = open("./temp/highscore.txt", "r")
    if f:
        hs = f.read().split(' ')
        d = hs[0]
        f.close()

    # print(type(score), type(hs[0]))
    if len(dead) > int(str(d)):
        d = str(len(dead))
        d1 = str(output_string.split(' ')[1])
        fai = 'NEW HIGHSCORE!!...\n'
        f = open("./temp/highscore.txt", "w")
        a = f"{d} {d1}"
        f.write(a)
    else:
        f = open("./temp/highscore.txt", "r")
        hs = f.read().split(' ')
        fai = f'BETTER LUCK NEXT TIME\nhighscore:{hs[0]}\ntime:{hs[1]}'

    pygame.draw.rect(win, 'black', pygame.Rect(0, 0, w, h))
    font = pygame.font.SysFont(name='arial', size=90)

    cv2.namedWindow("videoplayer", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("videoplayer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap3.read()
        if not ret:
            print("Reached end of video, exiting.")
            break
        cv2.imshow("videoplayer", frame)
        if (cv2.waitKey(30) & 0xFF == 27): break
    cap1.release()
    cv2.destroyAllWindows()

    # time.sleep(9000)
    exit()


            #self.current_sprite=len(self.sprites)


def main():
    clock=pygame.time.Clock()
    run=True
    moving_sprite=pygame.sprite.Group()
    p1=player()
    blist=[]

    hspancount=0
    zspancount=0
    enimy=[]
    droppos=[]
    b1droppos=[]
    sbdrop=[]
    smile=0
    dropsitms=[]
    dropdisplay=[]
    bulcount=10
    count=0
    shoot=False

    bosscount=0
    bossspancontroll=1000
    zombiespancontroll=1000
    hopperspanctrl=1000

    bultimes = 3
    pygame.mixer.Sound('./temp/sounds/background_sound.mp3').play().set_volume(0.1)
    hole1=(220, random.randint(0, 1000))
    hole2=(220, random.randint(0, 1000))
    hole3=(1500, random.randint(0, h-500))
    hole4=(1500, random.randint(0, h-500))
    hole=pygame.image.load('./temp/whole.png')
    hole=pygame.transform.scale(hole,[90,90])

    while run:
        if smile==0:
            p1.currenthead=head[5]
        elif smile==1:
            p1.currenthead=head[0]
            if count%120==0:
                p1.currenthead=head[5]
                smile=0

        clock.tick(fps)
        #pygame.display.set_mode((1090,1080),pygame.FULLSCREEN)
        #pygame.display.set_caption(f'FPS:{int(clock.get_fps())}   ALIEN SHOOTER')
        win.blit(background,(0,0,w,h))
        if p1.health/fps < 20 and p1.health/fps>0:
            win.blit(damage2, (0,0,w,h))
        elif p1.health/fps < 40 and p1.health/fps>20:
            win.blit(damage1, (0,0,w,h))

        win.blit(hole,hole1)
        win.blit(hole,hole2)
        win.blit(hole,hole3)
        win.blit(hole,hole4)

        for i,j in dead:
            win.blit(deadimg,(i,j))
        if hspancount> hopperspanctrl:
            hpos=random.choice([hole1,hole2,hole3,hole4])
            e = Hopper(hpos[0],hpos[1])
            enimy.append(e)
            moving_sprite.add(e)
            hspancount = 1
        else:hspancount += 1
        if zspancount>zombiespancontroll:
            e=zombie(random.choice(list(range(1000))),random.choice(list(range(10))))
            enimy.append(e)
            moving_sprite.add(e)
            zspancount=1
        else:zspancount += 1
        if bosscount>bossspancontroll:
            e=boss(random.choice(list(range(1000))),random.choice(list(range(10))))
            enimy.append(e)
            moving_sprite.add(e)
            bosscount=1
        else:bosscount += 1
        for i, j in b1droppos:
            win.blit(ammo1, (i, j))
            ammorect=deadimg.get_rect()
            ammorect.x=i
            ammorect.y=j
            if p1.rect.colliderect(ammorect):
               p1.gun1[1]+=50
               b1droppos.remove((i,j))
        for i,j in sbdrop:
            win.blit(sammo, (i, j))
            ammorect = deadimg.get_rect()
            ammorect.x = i
            ammorect.y = j
            if p1.rect.colliderect(ammorect):
                p1.gun2[1] += 20
                sbdrop.remove((i, j))
        for i, j in droppos:
            win.blit(heart, (i, j))
            heartrect=deadimg.get_rect()
            heartrect.x=i
            heartrect.y=j
            if p1.rect.colliderect(heartrect):
                if p1.health<100*fps:
                    p1.health+=3*fps
                    droppos.remove((i,j))
                else:
                    p1.health=100*fps
                    droppos.remove((i, j))

        if p1.gun==0:
            p1.original_image = img0
        elif p1.gun==1:
            p1.original_image = img1
        elif p1.gun==2:
            p1.original_image = img2



        if shoot:
            sound=''
            if p1.gun==2:
                sound="./temp/sounds/shotgun-firing-3-14483.mp3"
            elif p1.gun==1:
                sound="./temp/sounds/076415_light-machine-gun-m249-39827.mp3"
            else:
                sound='./temp/sounds/pistolfire.mp3'

            shotb=[]
            try:
                if p1.gun==2:
                    if count % 3 == 0:
                        for _ in range(4):
                            b=bullet(p1.posx, p1.posy)
                            b.angle+=float(_/10)
                            blist.append(b)
                        for _ in range(4):
                            b=bullet(p1.posx, p1.posy)
                            b.angle-=float(_/10)
                            blist.append(b)
                        shoot=False



                if count%3==0:
                    if bultimes!=0:
                        pygame.mixer.Sound(sound).play()
                        b = bullet(p1.posx, p1.posy)
                        blist.append(b)
                        bultimes-=1
                    else:shoot = False

            except Exception as e:
                print(e)
        ################################################################################## events



        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            #left, middle, right = pygame.mouse.get_pressed()
            #lr,rl=pygame.mouse.get_rel()
            if event.type == pygame.MOUSEBUTTONUP:
                smile=1


                try:
                    if p1.gun==0:
                        if p1.gun0[1]>0:
                            bultimes=1
                            p1.gun0[1]-=1
                            p1.gun0[0]-=1
                            bulcount -= 1
                            if bulcount<0 and p1.gun0[1]:
                                pygame.mixer.Sound('./temp/sounds/reloading.mp3').play().set_volume(0.5)
                                bulcount=10
                                p1.gun0[0]=10
                                continue
                            shoot=True
                        else:
                            pygame.mixer.Sound('./temp/sounds/reloading.mp3').play().set_volume(0.5)

                    elif p1.gun==1:
                        print('1')
                        if p1.gun1[1]>0:
                            bultimes=3
                            p1.gun1[1]-=1
                            p1.gun1[0]-=1
                            bulcount -= 1
                            if bulcount < 0 and p1.gun1[1]:
                                pygame.mixer.Sound(
                                    './temp/sounds/reloading.mp3').play().set_volume(0.5)
                                bulcount = 10
                                p1.gun1[0] = 10
                                continue
                            shoot=True
                        else:
                            pygame.mixer.Sound(
                                './temp/sounds/reloading.mp3').play().set_volume(0.5)


                    if p1.gun == 2:
                        print('2')
                        if p1.gun2[1] > 0:
                            bultimes = 1
                            p1.gun2[1] -= 1
                            p1.gun2[0] -= 1
                            bulcount -= 1
                            if bulcount < 0 and p1.gun2[1]:
                                pygame.mixer.Sound(
                                    './temp/sounds/reloading.mp3').play().set_volume(0.5)
                                bulcount = 10
                                p1.gun2[0] = 10
                                continue
                            shoot = True
                        else:
                            pygame.mixer.Sound(
                                './temp/sounds/reloading.mp3').play().set_volume(0.5)
                except Exception as e:
                    print(e)

            if event.type == pygame.MOUSEWHEEL:
                if p1.gun>=0:
                    if event.y==-1:
                        if p1.gun <= 2:
                            p1.gun+=1
                    if event.y==1:
                        if p1.gun >0:
                            p1.gun-=1

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_s]:
                p1.md()
            if keys_pressed[pygame.K_a]:
                p1.ml()
            if keys_pressed[pygame.K_ESCAPE]:
                run=False
            if keys_pressed[pygame.K_d]:
                p1.mr()
            if keys_pressed[pygame.K_w]:
                p1.mu()
            if keys_pressed[pygame.K_r]:
                pygame.mixer.Sound(
                    './temp/sounds/reloading.mp3').play()
                bulcount = 10
                p1.gun1[0] = 10
                p1.gun0[0] = 10
                p1.gun2[0] = 10
        moving_sprite.draw(win)
        moving_sprite.update(p1.posx, p1.posy)
        for i in blist:
            if i.x>w or i.x<10:
                blist.remove(i)
            elif i.y>h or i.y<10:
                blist.remove(i)
            else:
                i.move()


        try:
            for obj in enimy:
                if obj.rect.colliderect(p1.rect):
                    p1.currenthead=head[4]
                    # if obj.sound==True:
                    #     pygame.mixer.pause()
                if obj.name=='zombie':
                    if obj.rect.colliderect(p1.rect):

                        obj.sprites=zombieattack
                        obj.current_sprite=pygame.transform.rotate(obj.current_sprite,obj.angle)
                    else:
                        obj.sprites=zombiewalk



        except Exception:
            pass
        try:
            for obj1 in blist:
                for en in enimy:

                    if obj1.bul.colliderect(en.rect):
                        if en.name=='zombie':
                            en.health=0
                            blist.remove(obj1)

                        if en.health <= 0:
                            if en.drops:
                                droppos.append(en.deadpos())
                            if en.bdrops:
                                b1droppos.append(en.deadpos())
                            if en.sbdrops:
                                sbdrop.append(en.deadpos())
                            else: dead.append(en.deadpos())
                            moving_sprite.remove(en)
                            enimy.remove(en)
                        else:
                            if p1.gun==0:
                                en.health -= 11
                            if p1.gun==1:
                                en.health -= 50
                            if p1.gun==2:
                                en.health -= 100
                            blist.remove(obj1)
        except Exception:
            pass

        p1.draw(win)
        #################################health
        try:
            for en in enimy:
                if p1.rect.colliderect(en.rect):
                    p1.health-=5
                    if p1.health%200==0:
                        pygame.mixer.Sound('./temp/sounds/umph-47201.mp3').play()

        except Exception as e:
                pass

        if p1.health<=0:
            ex()



        #####################game bar
        pygame.draw.rect(win, '#800000',pygame.Rect(0,h-180,w,h),)
        pygame.draw.rect(win,'black',pygame.Rect(210,h-180,420,h-25),4,13)
        font = pygame.font.SysFont(name='arial', size=30)
        sym=' █'
        healthtxt=font.render(f'HEALTH: {sym*int((p1.health/fps)/10)}',True,'green')
        healthp=font.render(f'{int((p1.health/fps))}%',True,'black')
        win.blit(healthtxt,(226,h-165))
        win.blit(healthp,(226,h-139))
        pygame.draw.rect(win, 'black', pygame.Rect(700, h - 180, 100, h - 25), 4,13)
        font = pygame.font.SysFont(name='arial', size=50)
        score=font.render(f'{len(dead)}',True,'black')
        win.blit(score, (720, h - 160))
        pygame.draw.rect(win, 'black', pygame.Rect(w-720, h - 180,440, h - 25), 4,13)
        font = pygame.font.SysFont(name='arial', size=30)
        if p1.gun==0:
            pistol=pygame.image.load('./temp/ammo/0gunt.png')
            pistol = pygame.transform.scale(pistol, [80, 80])
            win.blit(pistol,(w-300, h - 280))
            bulrem = font.render(f'{p1.gun0[0]}/{int(p1.gun0[1]/10)}', True, 'orange')
            win.blit(bulrem, (w-700, h - 160))
            bultxt = font.render(f'{sym*p1.gun0[0]}', True, 'orange')
            win.blit(bultxt, (w-650, h - 160))
        if p1.gun==1:
            machinegun=pygame.image.load('./temp/ammo/1gunt.png')
            machinegun= pygame.transform.scale(machinegun, [80, 80])
            win.blit(machinegun, (w-300, h - 280))
            bulrem = font.render(f'{p1.gun1[0]}/{int(p1.gun1[1]/ 30)}', True, 'orange')
            win.blit(bulrem, (w-700, h - 160))
            bultxt = font.render(f'{sym *p1.gun1[0]}', True, 'orange')
            win.blit(bultxt, (w-650, h - 160))
        if p1.gun == 2:
            machinegun = pygame.image.load("./temp/ammo/shotgun.png")
            machinegun = pygame.transform.scale(machinegun, [80, 80])
            win.blit(machinegun, (w - 300, h - 280))
            bulrem = font.render(f'{p1.gun2[0]}/{int(p1.gun2[1] / 30)}', True, 'orange')
            win.blit(bulrem, (w - 700, h - 160))
            bultxt = font.render(f'{sym * p1.gun2[0]}', True, 'orange')
            win.blit(bultxt, (w - 650, h - 160))
        total_seconds = count // fps
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        #timer=font.render(f'{str(int((time.time() - startTime)/60))}:{str(int(time.time() - startTime))}', True, 'orange')
        timer=font.render(output_string, True, 'orange')
        win.blit(timer, (w-323, 120))

        #pygame.draw.rect(win, 'black', pygame.Rect(900, h - 180, 200, h - 25), 4, 13)
        pygame.draw.circle(win,'black',(900, h - 180),60)

        win.blit(p1.currenthead, (836, h - 270))


############  span controll
        if int(minutes)==0:
            hopperspanctrl=500
            zombiespancontroll=70
            bossspancontroll=5000
        elif int(minutes) == 1:
            hopperspanctrl=300
            zombiespancontroll=60
        elif int(minutes) == 2:
            zombiespancontroll = 60
            hopperspanctrl =100
        elif int(minutes) == 3:
            zombiespancontroll = 65
            hopperspanctrl = 65
        elif int(minutes) == 4:
            zombiespancontroll = 30
            hopperspanctrl = 65
            bossspancontroll = 1000
        elif int(minutes) == 5:
            zombiespancontroll = 50
            hopperspanctrl = 100
            bossspancontroll = 500
        elif int(minutes)==6:
            zombiespancontroll = 60
            hopperspanctrl = 150
            bossspancontroll = 150
        elif int(minutes)==7:
            zombiespancontroll = 10
            hopperspanctrl = 500
            bossspancontroll = 60
        elif int(minutes) == 8:
            break
        else:ex()

        count+=1
        pygame.display.update()

    pygame.quit()
if __name__=='__main__':
    cv2.namedWindow("videoplayer", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("videoplayer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret,frame=cap1.read()
        if not ret:
            print("Reached end of video, exiting.")
            break
        cv2.imshow("videoplayer",frame)
        if(cv2.waitKey(30) & 0xFF ==27):break
    cap1.release()
    cv2.destroyAllWindows()
    main()
    cv2.namedWindow("videoplayer", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("videoplayer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap2.read()
        if not ret:
            print("Reached end of video, exiting.")
            break
        cv2.imshow("videoplayer", frame)
        if (cv2.waitKey(30) & 0xFF == 27): break
    cap1.release()
    cv2.destroyAllWindows()
    cv2.namedWindow("videoplayer", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("videoplayer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap4.read()
        if not ret:
            print("Reached end of video, exiting.")
            break
        cv2.imshow("videoplayer", frame)
        if (cv2.waitKey(30) & 0xFF == 27): break
    cap1.release()
    cv2.destroyAllWindows()




