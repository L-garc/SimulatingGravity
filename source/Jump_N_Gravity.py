'''
This program makes a character (represented by a black square box) "jump" similar to how a person might, or a vertically thrown projectile
'''
import pygame

pygame.init()

ds = pygame.display.set_mode((1280, 720)) #Window size
pygame.display.set_caption('Gravity Testing') #Window title

clock = pygame.time.Clock()

#Defines colors using rgb values
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

gravity = -9.8 #Gravitational acceleration is negative
initVel = 14 #Inital velocity is positive
ratio = 45 #Sets the pixel to meter ratio (calculated as pixels per meter)
speed = 5 #Horizontal movement speed in meters per second

HeldIntervals = [] #Holds every delta y in the upward portion of the jump parabola
difVals = []
FallList = difVals #Will hold the reversed list of delta y's, for the downward portion
groundsList = [] #Ground object rects will automatically populate this list

'''
Equation for the height of an object in terms of time since it was launched
H(x) = -9.8(x**2) + bx + c
Height (after x seconds) = acceleration due to gravity + initial velocity of launched object + initial height (off the ground)
If there were other sources of acceleration (such as a gravitational feild of another object overhead) then you would add acceleration due to that object
'''
class Ground():
    def __init__(self, color, width, height, xpos, ypos):
        self.color = color
        self.w = width
        self.h = height
        self.x = xpos
        self.y = ypos
        self.Rec = pygame.Rect(self.x, self.y, self.w, self.h)
        groundsList.append(self.Rec)

    def blit(self):
        pygame.draw.rect(ds, self.color, self.Rec)
        
class Player():
    def __init__(self):
        self.color = black
        self.w = 20
        self.h = 20
        self.init_y = 680
        self.jumping = False
        self.falling = False
        self.grounded = True
        self.Rec = pygame.Rect(20, 680, self.w, self.h) #(x-pos, y-pos, width, height)
        #self.RecSearchArea = pygame.Rect(self.Rec.x, self.Rec.y, self.Rec.w, 720)
        self.dx = 0

    def blit(self):
        pygame.draw.rect(ds, self.color, self.Rec)

    def move(self, dx):
        self.Rec = self.Rec.move(dx, 0)
        #self.RecSearchArea = self.RecSearchArea.move(dx, 0)
        self.dx = dx

    def jump(self):
        self.jumping = True
        self.index = 0
        self.grounded = False
        self.init_y = self.Rec.y

    def detectWalls(self):
        #Stop the player from going off the screen (left side)
        if self.Rec.x < 0:
            self.Rec.update(0, self.Rec.y, self.Rec.w, self.Rec.h)
        #Stop the player from going off the screen (right side)
        elif self.Rec.x + self.Rec.w > 1280:
            self.Rec.update(1280 - self.Rec.w, self.Rec.y, self.Rec.w, self.Rec.h)

        #============================================================================================================================        
        collideIndex = self.Rec.collidelist(groundsList) #Returns index of rect object being collided with

        if collideIndex != -1: #-1 means no collisions, otherwise the index of the objcet collided with is stored here
            hitRec = groundsList[collideIndex] #The collided with object is stored here
            
            #If approaching from the left and the box is below the rect object's (ground) top
            if (self.dx > 0) and (self.Rec.y + self.Rec.h > hitRec.y +1): # For some reason the +1 makes the box not "teleport" to the top of a ground rec
                self.Rec.update((hitRec.x - self.w), self.Rec.y, self.Rec.w, self.Rec.h)
                
                #self.RecSearchArea.update((hitRec.x - self.w), self.RecSearchArea.y, self.RecSearchArea.w, self.RecSearchArea.h)

            #If approaching from the right
            elif (self.dx < 0) and (self.Rec.y + self.Rec.h > hitRec.y):
                self.Rec.update((hitRec.x + hitRec.w + self.w), self.Rec.y, self.Rec.w, self.Rec.h)
                #self.RecSearchArea.update((hitRec.x - self.w), self.RecSearchArea.y, self.RecSearchArea.w, self.RecSearchArea.h)
                
    def fall(self):
        if not self.grounded: #If Space bar is pressed
            intVal = (1/60) * self.index
            newY = H(intVal, self.init_y) #Calculate the height the box should be at, H(frame_interval, starting_Height)
            self.index += 1
            self.Rec.update(self.Rec.x, newY, self.Rec.w, self.Rec.h)
            
#Jumped the gun, should be placed in a new branch, this stops the box from falling to the ground after colliding with a ground object rect
    def newLanding(self):
        collideIndex = self.Rec.collidelist(groundsList)
        
        if collideIndex != -1:
            hitRec = groundsList[collideIndex]
            print(*hitRec)
            
            self.Rec.update(self.Rec.x, (hitRec.y - self.Rec.h), self.Rec.w, self.Rec.h)
            self.falling = False
            self.jumping = False
            self.grounded = True

    def Check4Grounds(self):
        tallestY = 720
        
        for rect in groundsList:
            if ((self.Rec.x < rect.x) and (rect.x < self.Rec.x + self.Rec.w)) or ((self.Rec.x < rect.x + rect.w) and (rect.x + rect.w < self.Rec.x + self.Rec.w)) or ((self.Rec.x > rect.x) and (self.Rec.x + self.Rec.w < rect.x + rect.w)):
                if rect.y < tallestY:
                    tallestY = rect.y

        return tallestY
            
#Anything we want to draw to screen call here
#For the box to appear "In front" of raised grounds, blit it after the other ground objects.
#To hide a box behind a ground object, blit it before the ground object
def blit2screen():
    baseGround.blit()
    elevG1.blit()
    player.blit()
    
#The equation for height of a projectile using gravity and a predetermined initial velocity (t refers to time in seconds)
def H(t, init_height):
    return (( (-gravity * (t**2)) - (initVel * t) )*ratio + init_height) #Use this because the origin is the top-left of the screen

player = Player() #Creates instance of Player class

baseGround = Ground(green, 1280, 20, 0, 700) #Creates instance of Ground class
elevG1 = Ground(green, 100, 220, 1180, 500) #Ground(color, width, height, x-pos, y-pos)

dx = 0 #Initialize horizontal movement to 0 (no change in x-position)
while True:
    if player.Rec.y > 680:
        player.grounded = True
        player.Rec.update(player.Rec.x, 680, player.Rec.w, player.Rec.h)
        
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.grounded:
                        player.jump()
                elif event.key == pygame.K_LEFT:
                    dx = -speed * (ratio / 60) #Divide by 60 because fps is limited to 60, position is updated every 60th of a second
                elif event.key == pygame.K_RIGHT:
                    dx = speed * (ratio / 60)
            if event.type == pygame.KEYUP:
                if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT)):
                    dx = 0
                    
    player.move(dx) #Horizontal movement (no momentum / friction)
    player.detectWalls() #Detects if a player meets a wall
    player.newLanding()
    player.fall() #Brings the box down unless box attribute grounded is true
    
    ds.fill(white) #White background
    blit2screen() #Draw objects on the screen

    pygame.display.flip() #Update screen
    clock.tick(60) #Limit frame rate to 60 fps (realworld 59 - 62 fps)

pygame.quit()
