import turtle
import math
import random

wn=turtle.Screen()
wn.bgcolor("black")
wn.title("MAZE GAME")
wn.setup(700,700)


#duvarlar oluşturulur
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

#oyuncu tanımlanır
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold=0

#oyuncunun hareketleri 
    def go_up(self):
        move_to_x=self.xcor()
        move_to_y=self.ycor() + 25
    
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        
    def go_down(self):
        move_to_x=self.xcor()
        move_to_y=self.ycor()-25
    
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
           
    def go_left(self):
        move_to_x=self.xcor()-25
        move_to_y=self.ycor() 
    
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        
    def go_right(self):
        move_to_x=self.xcor()+25
        move_to_y=self.ycor() 
    
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
            
    def is_collision(self,other):
        a=self.xcor()-other.xcor()
        b=self.xcor()-other.xcor()
        distance=math.sqrt((a ** 2)+(b ** 2))
        
        if distance<5:
            return True
        else:
            return False
        
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold=100
        self.goto(x, y)
        
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

#düşmanlar oluşturulur
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold=25
        self.goto(x, y)
        # düşmanların rastgele hareketleri
        self.direction=random.choice(["up","down","left","right"])
        
    def move(self):
        if self.direction == "up":
            dx=0
            dy=25
        elif self.direction ==" down":
            dx=0
            dy=-25
        elif self.direction == "left":
            dx=-25
            dy=0
        elif self.direction == "right":
            dx=25
            dy=0
        else:
            dx=0
            dy=0
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"
        move_to_x=self.xcor() + dx
        move_to_y=self.ycor() + dy
        
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction=random.choice(["up", "down", "left", "right"])
        
        turtle.ontimer(self.move, t=random.randint(100, 300))
   
    def is_close(self,other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance=math.sqrt((a ** 2) +(b ** 2))
        
        if distance < 75:
            return True
        else:
            return False
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

levels=[""]

level_1=[
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXE         XXXXX",
"X  XXXXXXX  XXXXXX  XXXXX",
"X       XX  XXXXXX  XXXXX",
"X       XX  XXX       EXX",
"XXXXXX  XX  XXX        XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X  XXX        XXXXT XXXXX",
"X  XXX  XXXXXXXXXXXXXXXXX",
"X         XXXXXXXXXXXXXXX",
"X                XXXXXXXX",  
"XXXXXXXXXXXX     XXXXX  X",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXX  XXXXXXXXXX         X",
"XXXE                    X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX   XXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX     XXXXXXXXXXX  XXXXX",
"XX          XXXX        X",
"XXXXE                   X",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]

treasures=[]
enemies=[]
levels.append(level_1)

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character=level[y][x]
            screen_x=-300 +(x * 25)
            screen_y=300 -(y * 25)
            
            if character=="X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
             
            if character=="P":
                player.goto(screen_x,screen_y)
            if character=="T":
                treasures.append(Treasure(screen_x,screen_y))
            if character=="E":
                enemies.append(Enemy(screen_x,screen_y))

pen=Pen()
player=Player()
walls=[]

setup_maze(levels[1])


turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")


# wn.tracer(0)

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)
while True:
    for treasure in treasures:
       if player.is_collision(treasure):
           player.gold += treasure.gold
           print("player gold:{}".format(player.gold))
           treasure.destroy()
           treasures.remove(treasure)
        
    for enemy in enemies:
        if player.is_collision(enemy):
            print("player dies!")
        
wn.update()
