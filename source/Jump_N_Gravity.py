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

gravity = -9.8 #Gravitational acceleration is negative
initVel = 14 #Inital velocity is positive

HeldIntervals = [] #Holds every delta y in the upward portion of the jump parabola
FallList = HeldIntervals #Holds the reversed list of delta y's
FallList.reverse() #Reverses the order of the delta y's for the downward portion of the jump parabola

'''
Equation for the height of an object in terms of time since it was launched
H(x) = -9.8(x**2) + bx + c
Height (after x seconds) = acceleration due to gravity + initial velocity of launched object + initial height (off the ground)
If there were other sources of acceleration (such as a gravitational feild of another object overhead) then you would add acceleration due to that object
'''

class Player():
    def __init__(self):
        self.color = black
        self.w = 20
        self.h = 20
        self.x = 20
        self.y = 700
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
            dH = HeldIntervals[self.index]
            self.Rec = self.Rec.move(0, -dH)
            if (self.index < len(HeldIntervals)-1):
                self.index += 1
            else:                       #After iterating through HeldIntervals
                self.jumping = False
                self.falling = True
                self.index = 1          #Starts at 1 not 0 because otherwise the box would be at its apex for 2 frames rather than 1
        elif self.falling:
            dH = FallList[self.index]
            self.Rec = self.Rec.move(0, dH)
            if (self.index < len(FallList)-1):
                self.index += 1
            else:
                self.falling = False
                self.grounded = True
        else:
            pass
#The equation for height of a projectile using gravity and a predetermined initial velocity (t refers to time in seconds)
def H(t):
    return ((gravity * (t**2)) + (initVel * t))

def findIntervals():
    apex = -initVel / (2 * gravity) #Calculates at what time the maximum height occurs (Only works for gravity and intial velocity, no other forces)
    index = 1 #Don't need height at time zero, height is the objects current position at t=0
    calc = True
    
    while calc:
        newInt = (1/60) * index #1/60 because I limited pygame to 60fps
        val = H( newInt ) 
        
        if (newInt <= apex): #Limits the list to height-at-each-interval up until the apex (since parabolas are symetrical we don't need to continue calc)
            HeldIntervals.append( val )
            index += 1
        else:
            calc = False

findIntervals() #Pre-calculates height of projectiles at certain intervals which line up with program frames
player = Player() #Creates instance of Player class

dx = 0
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.grounded:
                        player.jump()
                elif event.key == pygame.K_LEFT:
                    dx = -5 
                elif event.key == pygame.K_RIGHT:
                    dx = 5
            if event.type == pygame.KEYUP:
                if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT)):
                    dx = 0
    player.move(dx) #Horizontal movement (no momentum / friction)
    player.fall() #Brings the box down unless box attribute grounded is true
    
    ds.fill(white) #White background
    player.blit() #Draw the box on the screen

    pygame.display.flip() #Update screen
    clock.tick(60) #Limit frame rate to 60 fps (realworld 59 - 62 fps)

pygame.quit()
