# DISABLE INITIAL PYGAME CONSOLE PRINT
from os import environ

from pygame.mixer import pause
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# IMPORTS
import sys, pygame
from Border import BorderLine
from AgentRouter import AgentRouter
from FixedRouter import FixedRouter
from Device import Device
from Scene import Scene
import random

# INITIALIZE CONSTANTS
WINDOWSIZE = WIDTH, HEIGHT  = (1000, 1000)
BORDER_PADDING               = 50

#                           r   g   b   
BACKGROUND_COLOUR       = (200,200,200)
BORDER_COLOUR           = (  0,  0,  0)
BORDER_INFILL_COLOUR    = (255,255,255)
GRID_COLOUR             = (235,235,235)

#                                   r    g    b    a                                    
AGENT_ROUTER_COLOUR             = (230, 184,   0, 255)
AGENT_ROUTER_AREA_TRANSPARENCY  = (255, 224, 102,  60)
BOTH_ROUTER_AREA_TRANSPARENCY  = (220, 150, 102,  32)
FIXED_ROUTER_COLOUR             = ( 46, 184,  46, 255)
FIXED_ROUTER_AREA_TRANSPARENCY  = (153, 230, 153,  32)

GRID_COLUMNS    = 12
GRID_ROWS       = 12
MOVEMENT_SPEED  = 1

CELL_WIDTH = ( WIDTH  - (BORDER_PADDING * 2) ) / GRID_COLUMNS
CELL_HEIGHT = ( HEIGHT - (BORDER_PADDING * 2) ) / GRID_ROWS

DYNAMIC_SCENE = False

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
borderLines = [ BorderLine( BORDER_PADDING - 1     , BORDER_PADDING          , WIDTH - BORDER_PADDING + 1 , BORDER_PADDING              ),
                BorderLine( WIDTH - BORDER_PADDING , BORDER_PADDING - 1      , WIDTH - BORDER_PADDING     , HEIGHT - BORDER_PADDING + 1 ),
                BorderLine( BORDER_PADDING - 1     , HEIGHT - BORDER_PADDING , WIDTH - BORDER_PADDING + 1 , HEIGHT - BORDER_PADDING     ),
                BorderLine( BORDER_PADDING         , BORDER_PADDING - 1      , BORDER_PADDING             , HEIGHT - BORDER_PADDING + 1 )]



# Create our agent router object and place it at the center of the screen
agent = AgentRouter(5, 5, 2, False)

# Create our fixed router objects and place them at designated arbitrary locations on the screen inside the borders
fixedRouters = [FixedRouter( 2, 2, 3 ),
                FixedRouter( 9, 4, 3 )]

scenes = [Scene(GRID_COLUMNS, GRID_ROWS, not DYNAMIC_SCENE)]
currentScene = scenes[0]

currentScene.AddAgent(agent)
currentScene.AddFixedRouter(fixedRouters[0])
currentScene.AddFixedRouter(fixedRouters[1])

# for x in range(random.randint(6, 10)):
    # currentScene.AddDevice(Device(random.randint(0, GRID_COLUMNS - 1), random.randint(0, GRID_ROWS - 1), DYNAMIC_SCENE))

currentScene.AddDevice(Device(1, 5, DYNAMIC_SCENE))
currentScene.AddDevice(Device(6, 6, DYNAMIC_SCENE))
currentScene.AddDevice(Device(11, 3, DYNAMIC_SCENE))
currentScene.AddDevice(Device(9, 6, DYNAMIC_SCENE))
currentScene.AddDevice(Device(3, 9, DYNAMIC_SCENE))
currentScene.AddDevice(Device(2, 8, DYNAMIC_SCENE))

def main():

    paused = False

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    if(paused): 
                        paused = False
                        print("Resuming simulation...")
                    else: 
                        paused = True
                        print("Pausing simulation...")
                if event.key == pygame.K_e:
                    currentScene.ToggleExploration()
                if event.key == pygame.K_r:
                    currentScene.ShuffleAgentRouters()
                    print("Randomizing agent location...")

        
        if(not paused):
            # Update the screen Contents
            Update()
        
        # Render the Screen Contents
        Render()


def Update():
    currentScene.Update()

def Render():
    screen.fill(BACKGROUND_COLOUR)              # Fill the background of the windows to our predetermined colour
    FillInsideBorder(borderLines,screen)        # Fill inside the borders with our backround colour

    DrawScene(screen, currentScene)
    
    pygame.display.update()                     # update the display with the next frame
    fps.tick(1000)                                # Move to the next tick given 144 frames per second

def DrawBorders(borderLines,screen):
    for line in borderLines:
        pygame.draw.line(screen,        # Surface to draw to
                        BORDER_COLOUR,  # colour of line
                        ( line.startX , line.startY ),     # Start location of line
                        ( line.endX   , line.endY   ),     # end location of line
                        4)              # Width of line

def FillInsideBorder(borderLines,screen):
    points = [  (borderLines[0].startX, borderLines[0].startY ),     # Top Left
                (borderLines[0].endX,   borderLines[0].endY   ),     # Top Right
                (borderLines[2].endX,   borderLines[2].endY   ),     # Bottom Right
                (borderLines[2].startX, borderLines[2].startY )]     # Bottom Left
    pygame.draw.polygon(
        screen,                 # Screen to draw to
        BORDER_INFILL_COLOUR,   # Colour to graw the polygon with
        points)                 # points of polygon to draw          

def DrawScene(screen, scene):

    DrawGrid(screen, scene.columns, scene.rows) # Draw the grids on the screen

    routerSurface.fill((0,0,0,0))

    DrawRouters(scene.fixedRouters + scene.agentRouters) # Draw the fxed routers on screen
    DrawDevices(scene.devices) # Draw the devices on screen

    screen.blit(routerSurface, (0,0))

    DrawPadding(screen) # Draw the grey padding on the screen
    DrawBorders(borderLines, screen) # Draw the black borders around the scene
    DrawText(screen)

def DrawText(screen):
    screen.blit(quitText,(20,20)) # Draw the "Exit" text on screen
    
    rawStatText = ["","",""]

    rawStatText[0] = "Surface Coverage: " + str(currentScene.state.coverage)
    rawStatText[1] = "Interference: " + str(currentScene.state.interference)
    rawStatText[2] = "Devices Serviced: " + str(currentScene.state.devicesServiced)

    for i in range(len(rawStatText)):
        renderedStats = pygame.font.SysFont('arial', 16, True).render(rawStatText[i], False, (0, 0, 0))
        screen.blit(renderedStats,(20 + (200 * i),HEIGHT - 40))

def DrawDevices(devices):
    deviceSurface = pygame.Surface(WINDOWSIZE, pygame.SRCALPHA)

    #print(len(devices))

    for device in devices:

        screenX, screenY = GridLocationToScreenLocation(device.xPos, device.yPos)

        pygame.draw.circle(deviceSurface, (device.COLOUR), (screenX, screenY), device.radius) 

    routerSurface.blit(deviceSurface, (0,0))

def DrawPadding(screen):
    
    pygame.draw.rect(
        screen,                 # Screen to draw to
        BACKGROUND_COLOUR,      # Colour to graw the polygon with
        (0, 0, BORDER_PADDING, HEIGHT)) # points of polygon to draw

    pygame.draw.rect(
        screen,                 # Screen to draw to
        BACKGROUND_COLOUR,      # Colour to graw the polygon with
        (WIDTH - BORDER_PADDING, 0, BORDER_PADDING, HEIGHT)) # points of polygon to draw

    pygame.draw.rect(
        screen,                 # Screen to draw to
        BACKGROUND_COLOUR,      # Colour to graw the polygon with
        (BORDER_PADDING, 0, WIDTH - (BORDER_PADDING * 2), BORDER_PADDING)) # points of polygon to draw

    pygame.draw.rect(
        screen,                 # Screen to draw to
        BACKGROUND_COLOUR,      # Colour to graw the polygon with
        (BORDER_PADDING, HEIGHT - BORDER_PADDING, WIDTH - (BORDER_PADDING * 2), BORDER_PADDING)) # points of polygon to draw

def DrawGrid(screen, columns, rows):
    
    # Draw Vertical Grid Lines
    for x in range(columns - 1):
        x = x + 1
        pygame.draw.line(
            screen,        # Surface  to draw to
            GRID_COLOUR,   # Colour of line
            ( BORDER_PADDING + ( CELL_WIDTH * x ), BORDER_PADDING ),           # Start location of line
            ( BORDER_PADDING + ( CELL_WIDTH * x ), HEIGHT - BORDER_PADDING ),  # end location of line
            2)             # Width of line
    # Draw Horizontal Grid Lines
    for y in range(rows - 1):
        y = y + 1
        pygame.draw.line(
            screen,          # Surface to draw to
            GRID_COLOUR,     # Colour of line
            ( BORDER_PADDING, BORDER_PADDING + (CELL_HEIGHT * y) ),         # Start location of line
            ( WIDTH - BORDER_PADDING, BORDER_PADDING + (CELL_HEIGHT * y) ), # end location of line
            2)               # Width of line

def GridLocationToScreenLocation(xPos, yPos):

    screenX = BORDER_PADDING + (xPos * CELL_WIDTH) + (CELL_WIDTH / 2.0)
    screenY = BORDER_PADDING + (yPos * CELL_HEIGHT) + (CELL_HEIGHT / 2.0)

    return screenX, screenY

def DrawRouters(routers):
    # Create new Surface to draw the Routers to
    transparentSurface = pygame.Surface(WINDOWSIZE, pygame.SRCALPHA)
    grid = currentScene.state.GetGrid()

    screenX = 0
    screenY = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):

            fixedService = grid[row][col]["FixedService"]
            agentService = grid[row][col]["AgentService"]

            if(agentService and fixedService):
                screenX, screenY = GridLocationToScreenLocation(col, row)

                pygame.draw.rect(
                        transparentSurface,                 # Screen to draw to
                        BOTH_ROUTER_AREA_TRANSPARENCY,      # Colour to graw the polygon with
                        (screenX - (CELL_WIDTH / 2), screenY - (CELL_WIDTH / 2), CELL_WIDTH, CELL_HEIGHT)) # points of polygon to draw
            elif(agentService):
                screenX, screenY = GridLocationToScreenLocation(col, row)

                pygame.draw.rect(
                        transparentSurface,                 # Screen to draw to
                        AGENT_ROUTER_AREA_TRANSPARENCY,      # Colour to graw the polygon with
                        (screenX - (CELL_WIDTH / 2), screenY - (CELL_WIDTH / 2), CELL_WIDTH, CELL_HEIGHT)) # points of polygon to draw 
            elif(fixedService):
                screenX, screenY = GridLocationToScreenLocation(col, row)

                pygame.draw.rect(
                        transparentSurface,                 # Screen to draw to
                        FIXED_ROUTER_AREA_TRANSPARENCY,      # Colour to graw the polygon with
                        (screenX - (CELL_WIDTH / 2), screenY - (CELL_WIDTH / 2), CELL_WIDTH, CELL_HEIGHT)) # points of polygon to draw

    routerSurface.blit(transparentSurface, (0,0))
    
    # Draw the opaque parts of the fixed routers to our transparentSurface then display on the screen
    for router in routers:

        screenX, screenY = GridLocationToScreenLocation(router.xPos, router.yPos)

        pygame.draw.circle(transparentSurface, router.COLOUR, (screenX, screenY), router.radius)
    
    routerSurface.blit(transparentSurface, (0,0))

if __name__ == '__main__':
    main()