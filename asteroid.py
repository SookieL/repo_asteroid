from re import A
from turtle import position
from if3_game.engine import Sprite, Game, Layer, Text
from random import choice 
from pyglet import window, font
from random import randint
from math import cos, sin, radians
RESOLUTION = (800, 600)
LIFE_MAX = 5 

class AsteroidGame(Game): 
    def __init__(self):
        super().__init__()

        
# creation des layers
        self.bg_layer = Layer()
        self.add(self.bg_layer)

        self.game_layer = Layer()
        self.add(self.game_layer)

        self.ui_layer = UILayer()
        self.add(self.ui_layer)
# creer les element de jeux 
        position = (RESOLUTION[0]/2, RESOLUTION[1]/2)
        self.spaceship = Spaceship(position)
        

        self.game_layer.add(self.spaceship) # ajouter au game_layer 
        self.ui_layer.spaceship = self.spaceship

        

        for n in range(3): 
            x = randint(0, RESOLUTION[0])
            y = randint(0, RESOLUTION[1])
            position=(x , y)

            sx = randint(-300, 300)
            sy = randint(-300, 300)
            speed=(sx, sy)


            asteroid=Asteroid(position, speed)
            self.game_layer.add(asteroid)

        bg = Sprite("images/bg.png", (0,0)) 
        self.bg_layer.add(bg)   

class UILayer(Layer):  
    def __init__(self):
        super().__init__()
        
        
        
        self.spaceship = None

        
        self.lifes =[]
        image = "images/life.png"

        for n in range(LIFE_MAX): 
            x= 780 - n * 24
            y = 580
            anchor =(8, 8)
            s=Sprite(image, (x, y), anchor = anchor )
            
            
            self.add(s)
            self.lifes.append(s)
        
    def update(self, dt):
        super().update(dt)

        for n in range(len(self.lifes)): 
            if n < self.spaceship.life:
                self.lifes[n].opacity = 255 
            else: 
                self.lifes[n].opacity = 0


            if self.spaceship.life <=0 :
                text= Text("GAME OVER ", (400, 560), 36, anchor='center')
                self.add(text)

class SpaceItem(Sprite):
    def __init__(self,image, position, anchor, speed=(0,0), rotation_speed=0):
        
        super().__init__(image, position ,anchor = anchor)

        self.speed= speed

        self.rotation_speed= rotation_speed

    def update(self, dt): #dt = delta time, l'ecart entre 2 frame 
        super().update(dt)

        #position actuel 
        pos_x = self.position[0]#position du Spaceship en position X << horizontal 
        pos_y = self.position[1]#position du Spaceship en position Y << vertical 
        
        #calcul de deplacement 
        move =(self.speed[0] * dt, self.speed[1]* dt)# calculer le move ( distance = vitesse * le temps )
        
        # Application du deplacement 
        pos_x += move[0]
        pos_y += move[1]

        
        if pos_x > RESOLUTION[0] + 32:
            pos_x = -32

        elif pos_x <-32 :
            pos_x = RESOLUTION[0] +32


        if pos_y > RESOLUTION[1] + 32 :
            pos_y= -32
        elif pos_y  < -32:
            pos_y = RESOLUTION[1] + 32

        self.position = (pos_x, pos_y)

        # gerer la rotation 
        self.rotation += self.rotation_speed * dt 

class Spaceship(SpaceItem):


    def __init__(self, position):
        image ="images/spaceship.png"
        anchor=(32, 32)
        
        super().__init__(image, position, anchor)
        self.velocity = 0
        self.invulnerability = False 
        self.chrono = 0
        self.life = 3 

    def update(self, dt):
        if self.invulnerability == True: 
            self.opacity = 125
            self.chrono += dt
            if self.chrono >= 3:
                self.invulnerability = False
                self.chrono = 0 
                
                #print(self.chrono)
        else:
            self.opacity = 255
        dsx = cos(radians(self.rotation)) * self.velocity 
        dsy = sin(radians(self.rotation)) * self.velocity *-1
        sx = self.speed[0] + dsx 
        sy =  self.speed[1] + dsy
        self.speed = (sx, sy)
        super().update(dt)

    def on_key_press(self, key, modifiers): # les modifieurs sont des touches appuyé ensemble comme "ctrl + a"  
        if key == window.key.LEFT :
            self.rotation_speed = -50

        elif key == window.key.RIGHT:
            self.rotation_speed= 50

        elif key == window.key.UP:
            self.velocity = 5  

        elif key == window.key.SPACE:
            self.spawn_bullet()

    #elif key == window.key.DOWN:
    #self.velocity = -5  
    def on_key_release(self, key, modifiers): # les modifieurs sont des touches appuyé ensemble comme "ctrl + a"  
        
        if key == window.key.LEFT and self.rotation_speed < 0:
            self.rotation_speed = 0

        elif key == window.key.RIGHT and self.rotation_speed > 0:
            self.rotation_speed= 0

        elif key == window.key.UP:
            self.velocity = 0
    #elif key == window.key.DOWN:
    #    self.velocity = 0

    def spawn_bullet(self):

        bullet_velocity = 100 

        sx = cos(radians(self.rotation)) * bullet_velocity
        sy = sin(radians(self.rotation)) * bullet_velocity * -1
        
        bullet_speed =(
            self.speed[0] + sx, self.speed[1] + sy
        )

        x = cos(radians(self.rotation))*40
        y = sin(radians(self.rotation)) * 40 * -1

        bullet_position = (self.position[0] + x ,  self.position[1] + y)

        bullet = Bullet(bullet_position, bullet_speed)
        self.layer.add(bullet)

    def on_collision(self, other):
        if isinstance(other, Asteroid):
            self.destroy()

    def destroy(self):
        if self.invulnerability == False: 
            self.invulnerability = True
            self.life -= 1

            if self.life <= 0:
                super().destroy()

class Asteroid(SpaceItem):
    def __init__(self, position, speed, level=3):
        self.level = level
        if level == 3: 
            image ="images/asteroid128.png"
            anchor=(64, 64)

        elif level == 2: 
            image ="images/asteroid64.png"
            anchor=(32, 32)
        else:
            
            image ="images/asteroid32.png"
            anchor=(16, 16)

        
        rotation_speed=50
        super().__init__(image, position, anchor,  speed, rotation_speed)
    
    def destroy(self):       
        if self.level> 1 :
            for n in range(2): 
                sx=randint(-300, 300)
                sy=randint(-300, 300)
                speed= (sx, sy)
                level=self.level-1

                asteroid = Asteroid(self.position, speed, level = level)
                self.layer.add(asteroid)
        super().destroy()

class Bullet(SpaceItem):
    def __init__ (self, position , speed):

        image= "images/bullet.png"
        
        anchor = (8, 8)

        rotation_speed=100
        super().__init__(image, position, anchor, speed, rotation_speed)

        self.life_time = 0

    def update(self, dt):
        super().update(dt)

        self.life_time += dt 
        if self.life_time >= 3: 
            self.destroy()



    def on_collision(self, other):
        if isinstance(other, Asteroid):

            self.destroy() 
            other.destroy() 



