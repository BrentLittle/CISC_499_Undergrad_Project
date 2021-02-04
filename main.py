# DISABLE INITIAL PYGAME CONSOLE PRINT
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# IMPORTS
import sys, pygame
from pynput.keyboard import Key, Controller
from Border import BorderLine
from AgentRouter import AgentRouter
from FixedRouter import FixedRouter

# INITIALIZE CONSTANTS
WINDOWSIZE = WIDTH, HEIGHT  = (1000, 800)
BORDERPADDING               = 50

#                           r   g   b   
BACKGROUND_COLOUR       = (200,200,200)
BORDER_COLOUR           = (  0,  0,  0)
BORDER_INFILL_COLOUR    = (255,255,255)
GRID_COLOUR             = (235,235,235)

#                                   r    g    b    a                                    
AGENT_ROUTER_COLOUR             = (230, 184,   0, 255)
AGENT_ROUTER_AREA_TRANSPARENCY  = (255, 224, 102,  50)
FIXED_ROUTER_COLOUR             = ( 46, 184,  46, 255)
FIXED_ROUTER_AREA_TRANSPARENCY  = (153, 230, 153,  32)

GRID_COLUMNS    = 40
GRID_ROWS       = 32
MOVEMENT_SPEED  = 1

# Initialize pygame and create window with no frame of a given size
pygame.init()
pygame.font.init()

# create some text to display on screen how to quit the simulation
quitText= pygame.font.SysFont('arial', 16, True).render('Press \'ESC\' to Exit', False, (0, 0, 0))

# Create our display windows and a drawing surface for our routers so they can be semt-transparent on the screen
screen = pygame.display.set_mode( WINDOWSIZE, pygame.NOFRAME  )
routerSurface =   pygame.Surface( WINDOWSIZE, pygame.SRCALPHA )
peopleSurface =   pygame.Surface( WINDOWSIZE, pygame.SRCALPHA )
#                                             ^^^^^^^^^^^^^^^
#                                             Allows for the surface to accept alpha values for objects to draw in the screen

# setup a clock to limit the number of frames per second
fps = pygame.time.Clock()

#           UP     DOWN   LEFT   RIGHT
movement = [False, False, False, False]

# Fill borderLines in the following order:
    # TOP, RIGHT, BOTTOM, LEFT
        # Left and Right Lines have start at the top of screen and end towards bottom of screen
        # Top and Bottom Lines have start at Left of screen and end towards the Right of screen.
borderLines = [ BorderLine( BORDERPADDING - 1     , BORDERPADDING          , WIDTH - BORDERPADDING + 1 , BORDERPADDING              ),
                BorderLine( WIDTH - BORDERPADDING , BORDERPADDING - 1      , WIDTH - BORDERPADDING     , HEIGHT - BORDERPADDING + 1 ),
                BorderLine( BORDERPADDING - 1     , HEIGHT - BORDERPADDING , WIDTH - BORDERPADDING + 1 , HEIGHT - BORDERPADDING     ),
                BorderLine( BORDERPADDING         , BORDERPADDING - 1      , BORDERPADDING             , HEIGHT - BORDERPADDING + 1 )]

# Create our agent router object and place it at the center of the screen
agent = AgentRouter((WIDTH / 2), (HEIGHT / 2), 200, borderLines )

# Create our fixed router objects and place them at designated arbitrary locations on the screen inside the borders
fixedRouters = [FixedRouter( 250        , 250         , 200 ),
                FixedRouter( WIDTH - 250, 250         , 200 ),
                FixedRouter( 250        , HEIGHT - 250, 200 ),
                FixedRouter( WIDTH - 250, HEIGHT - 250, 200 )]


def main():
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    movement[0] = True
                if event.key == pygame.K_DOWN:
                    movement[1] = True
                if event.key == pygame.K_LEFT:
                    movement[2] = True
                if event.key == pygame.K_RIGHT:
                    movement[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    movement[0] = False
                if event.key == pygame.K_DOWN:
                    movement[1] = False
                if event.key == pygame.K_LEFT:
                    movement[2] = False
                if event.key == pygame.K_RIGHT:
                    movement[3] = False
        
        # Update the screen Contents
        Update()
        
        # Render the Screen Contents
        Render()


def Update():
    if MOVEMENT_SPEED > agent.DistanceToTopBorder():
        movement[0] == False
    elif movement[0] == True:
        agent.yPos -= MOVEMENT_SPEED
    
    if MOVEMENT_SPEED > agent.DistanceToBottomBorder():
        movement[1] == False
    elif movement[1] == True:
        agent.yPos += MOVEMENT_SPEED

    if MOVEMENT_SPEED > agent.DistanceToLeftBorder():
        movement[2] == False
    elif movement[2] == True:
        agent.xPos -= MOVEMENT_SPEED

    if MOVEMENT_SPEED > agent.DistanceToRightBorder():
        movement[3] == False
    elif movement[3] == True:
        agent.xPos += MOVEMENT_SPEED

def Render():
    screen.fill(BACKGROUND_COLOUR)              # Fill the background of the windows to our predetermined colour
    FillInsideBorder(borderLines,screen)        # Fill inside the borders with our backround colour
    DrawGrid(screen, GRID_COLUMNS, GRID_ROWS)   # Draw the grid lines onto our screen
    DrawBorders(borderLines, screen)            # Draw the borders borders onto the screen
    screen.blit(quitText,(20,20))               # Display the textsurface we want to show on the screen
    
    routerSurface.fill((0,0,0,0))               # Clear the routerSurface 
    
    RenderRouters()                             # Draw the routers onto the routerSurface
    
    screen.blit(routerSurface, (0,0))           # Draw the router Surface onto our screen
    
    pygame.display.update()                     # update the display with the next frame
    fps.tick(250)                               # Move to the next tick given 144 frames per second

def DrawBorders(borderLines,screen):
    for line in borderLines:
        pygame.draw.line(screen,        # Surface to draw to
                        BORDER_COLOUR,  # colour of line
                        ( line.startX , line.startY ),     # Start location of line
                        ( line.endX   , line.endY   ),     # end location of line
                        4)              # Width of line

def FillInsideBorder(borderLines,screen):
    points = [  ( borderLines[0].startX, borderLines[0].startY ),     # Top Left
                ( borderLines[0].endX,   borderLines[0].endY   ),     # Top Right
                ( borderLines[2].endX,   borderLines[2].endY   ),     # Bottom Right
                 (borderLines[2].startX, borderLines[2].startY )]     # Bottom Left
    pygame.draw.polygon(
        screen,                 # Screen to draw to
        BORDER_INFILL_COLOUR,   # Colour to graw the polygon with
        points)                 # points of polygon to draw          

def DrawGrid(screen, columns, rows):
    horizCellDimension = ( WIDTH  - (BORDERPADDING * 2) ) / columns
    vertiCellDimension = ( HEIGHT - (BORDERPADDING * 2) ) / rows
    
    # Draw Vertical Grid Lines
    for x in range(columns - 1):
        x = x + 1
        pygame.draw.line(
            screen,        # Surface  to draw to
            GRID_COLOUR,   # Colour of line
            ( BORDERPADDING + ( horizCellDimension * x ), BORDERPADDING ),           # Start location of line
            ( BORDERPADDING + ( horizCellDimension * x ), HEIGHT - BORDERPADDING ),  # end location of line
            2)             # Width of line
    # Draw Horizontal Grid Lines
    for y in range(rows - 1):
        y = y + 1
        pygame.draw.line(
            screen,          # Surface to draw to
            GRID_COLOUR,     # Colour of line
            ( BORDERPADDING, BORDERPADDING + (vertiCellDimension * y) ),         # Start location of line
            ( WIDTH - BORDERPADDING, BORDERPADDING + (vertiCellDimension * y) ), # end location of line
            2)               # Width of line

def RenderRouters():
    # Create new Surface to draw the Routers to
    transparentSurface = pygame.Surface(WINDOWSIZE, pygame.SRCALPHA)
    
    # Draw the translucent part of the fixed routers to our transparentSurface then display on the screen
    for fixedRouter in fixedRouters:
        pygame.draw.circle(transparentSurface, (FIXED_ROUTER_AREA_TRANSPARENCY), (fixedRouter.xPos, fixedRouter.yPos), fixedRouter.connectionRadius) 
    routerSurface.blit(transparentSurface, (0,0))
    
    # Draw the translucent part of the Agent router to our transparentSurface then display on the screen
    pygame.draw.circle(transparentSurface, (AGENT_ROUTER_AREA_TRANSPARENCY), (agent.xPos, agent.yPos), agent.connectionRadius)
    routerSurface.blit(transparentSurface, (0,0))
    
    # Draw the opaque parts of the fixed routers to our transparentSurface then display on the screen
    for fixedRouter in fixedRouters:
        pygame.draw.circle(transparentSurface, FIXED_ROUTER_COLOUR, (fixedRouter.xPos, fixedRouter.yPos), fixedRouter.radius)
        pygame.draw.circle(transparentSurface, FIXED_ROUTER_COLOUR, (fixedRouter.xPos, fixedRouter.yPos), fixedRouter.connectionRadius, 2)
    
    # Draw the opaque parts of the Agent router on top of everything else then display on the screen
    pygame.draw.circle(transparentSurface, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.radius)
    pygame.draw.circle(transparentSurface, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.connectionRadius, 2)
    routerSurface.blit(transparentSurface, (0,0))

if __name__ == '__main__':
    main()