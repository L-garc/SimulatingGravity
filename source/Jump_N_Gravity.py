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

'''
Equation for the height of an object in terms of time since it was launched
H(x) = -9.8(x**2) + bx + c
Height (after x seconds) = acceleration due to gravity + initial velocity of launched object + initial height (off the ground)
If there were other sources of acceleration (such as a gravitational feild of another object overhead) then you would add acceleration due to that object
'''
class Ground():
    def __init__(self):
        self.color = green
        self.w = 1280
        self.h = 20
        self.x = 0
        self.y = 700
        self.Rec = pygame.Rect(self.x, self.y, self.w, self.h)

    def blit(self):
        pygame.draw.rect(ds, self.color, self.Rec)
        
class Player():
    def __init__(self):
        self.color = black
        self.w = 20
        self.h = 20
        self.x = 20
        self.y = 680
        self.jumping = False
        self.falling = False
        self.grounded = True
        self.Rec = pygame.Rect(self.x, self.y, self.w, self.h)

    def blit(self):
        pygame.draw.rect(ds, self.color, self.Rec)

    def move(self, dx):
        self.Rec = self.Rec.move(dx, 0)

    def jump(self):
        self.jumping = True
        self.index = 0
        self.grounded = False

    def fall(self):
        if self.jumping: #If Space bar is pressed
            dH = difVals[self.index] * ratio #Calculate the height the box should be at, then apply pixel : meter ratio
            self.Rec = self.Rec.move(0, -dH)
            if (self.index < len(difVals)-1):
                self.index += 1
            else:                       #After iterating through HeldIntervals
                self.jumping = False
                self.falling = True
                self.index = 1          #Starts at 1 not 0 because otherwise the box would be at its apex for 2 frames rather than 1
        elif self.falling:
            dH = FallList[self.index] * ratio
            self.Rec = self.Rec.move(0, dH)
            if (self.index < len(FallList)-1):
                self.index += 1
            else:
                self.falling = False
                self.grounded = True
        else:
            pass
       
#Anything we want to draw to screen call here
def blit2screen():
    player.blit()
    ground.blit()
    
#The equation for height of a projectile using gravity and a predetermined initial velocity (t refers to time in seconds)
def H(t):
    return ((gravity * (t**2)) + (initVel * t))

def findIntervals():
    apex = -initVel / (2 * gravity) #Calculates at what time the maximum height occurs (Only works for gravity and intial velocity, no other forces)
    index = 0
    calc = True
    
    while calc:
        newInt = (1/60) * index #1/60 because I limited pygame to 60fps
        val = H( newInt ) 
        
        if (newInt <= apex): #Limits the list to height-at-each-interval up until the apex (since parabolas are symetrical we don't need to continue calc)
            HeldIntervals.append( val )
            index += 1
        else:
            calc = False

    for i in range(0,len(HeldIntervals)-1):
        difVals.append( HeldIntervals[i+1] - HeldIntervals[i])

    
     #FallList is defined by difVals, since we populate difVals here, and we want FallList reversed, it must be done here
            #==========================================================================================================================================================================

findIntervals() #Pre-calculates height of projectiles at certain intervals which line up with program frames
FallList = difVals[::-1] #This method of reversing a list prevents the original "difVals" from also being reversed, reverse() reverses both

player = Player() #Creates instance of Player class
ground = Ground() #Creates instance of Ground class

dx = 0 #Initialize horizontal movement to 0 (no change in x-position)
while True:
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
    player.fall() #Brings the box down unless box attribute grounded is true
    
    ds.fill(white) #White background
    blit2screen() #Draw objects on the screen

    pygame.display.flip() #Update screen
    clock.tick(60) #Limit frame rate to 60 fps (realworld 59 - 62 fps)

pygame.quit()
