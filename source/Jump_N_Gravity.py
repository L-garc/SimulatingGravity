'''
This program makes a character (represented by a black square box) "jump" similar to how a person might, or a vertically thrown projectile

This program assumes no change in elevation, the displacement of the block (vertically) will be zero after 
'''
import pygame

pygame.init()

ds = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Gravity Testing')

clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)

gravity = -9.8 #Gravitational acceleration is negative
initVel = 20 #Inital velocity is positive

HeldIntervals = []
FallList = HeldIntervals
FallList.reverse()

'''
Equation for the height of an object in terms of time since it was launched
H(x) = -9.8(x**2) + ax + b
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

    def jump(self):
        self.jumping = True
        self.index = 0
        self.grounded = False

    def fall(self):
        if self.jumping:
            dH = HeldIntervals[self.index]
            self.Rec = self.Rec.move(0, -dH)
            if (self.index < len(HeldIntervals)-1):
                self.index += 1
            else:
                self.jumping = False
                self.falling = True
                self.index = 1
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

def H(t):
    return ((gravity * (t**2)) + (initVel * t))

def findIntervals():
    apex = -initVel / (2 * gravity) #Calculates at what time the maximum height occurs
    index = 1
    calc = True
    
    while calc:
        newInt = (1/60) * index #1/60 because I limited pygame to 60fps
        val = H( newInt ) 
        
        if (newInt <= apex): #Limits the list to height-at-each-interval up until the apex (since parabolas are symetrical we don't need to continue calc)
            HeldIntervals.append( val )
            index += 1
        else:
            calc = False

findIntervals()
player = Player()

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.grounded:
                        player.jump()
                    
    player.fall()
    
    ds.fill(white)
    player.blit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
