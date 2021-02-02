# DISABLE INITIAL PYGAME CONSOLE PRINT
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# IMPORTS
import sys, pygame
from Border import BorderLine
from AgentRouter import AgentRouter
from FixedRouter import FixedRouter

# INITIALIZE CONSTANTS
WINDOWSIZE = WIDTH, HEIGHT  = (1000, 800)
BORDERPADDING               = 50

BACKGROUND_COLOUR       = (200,200,200)
BORDER_COLOUR           = (  0,  0,  0)
BORDER_INFILL_COLOUR    = (255,255,255)
GRID_COLOUR             = (235,235,235)

AGENT_ROUTER_COLOUR             = (204,   0,   0, 255)
AGENT_ROUTER_AREA_TRANSPARENCY  = (255, 128, 128,  63)
FIXED_ROUTER_COLOUR             = ( 46, 184,  46, 255)
FIXED_ROUTER_AREA_TRANSPARENCY  = (153, 230, 153,  63)

GRID_COLUMNS    = 40
GRID_ROWS       = 32

# Initialize pygame and create window with no frame of a given size
pygame.init()
pygame.font.init()

# create some text to display on screen how to quit the simulation
quitText= pygame.font.SysFont('arial', 16, True).render('Press \'ESC\' to Exit', False, (0, 0, 0))

# Create our display windows and a drawing surface for our routers so they can be semt-transparent on the screen
screen = pygame.display.set_mode( WINDOWSIZE, pygame.NOFRAME )
routerSurface = pygame.Surface( WINDOWSIZE, pygame.SRCALPHA )

# setup a clock to limit movement speeds
fps = pygame.time.Clock()

        #   UP     DOWN   LEFT   RIGHT
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
agent = AgentRouter(WIDTH / 2, HEIGHT / 2, 200)


def main():
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP or event.key == ord('w'):
                    movement[0] = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    movement[1] = True
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    movement[2] = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    movement[3] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    movement[0] = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    movement[1] = False
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    movement[2] = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    movement[3] = False
        
        # Update the screen Contents
        Update()
        
        # Render the Screen Contents
        Render()

        


def Update():
    if movement[0] == True: # Move agent UP
        agent.yPos -= 1
    if movement[1] == True: # Move agent DOWN
        agent.yPos += 1
    if movement[2] == True: # Move agent LEFT
        agent.xPos -= 1
    if movement[3] == True: # Move agent RIGHT
        agent.xPos += 1

def Render():
    
    screen.fill(BACKGROUND_COLOUR)              # Fill the background of the windows to our predetermined colour
    FillInsideBorder(borderLines,screen)        # Fill inside the borders with our backround colour
    DrawGrid(screen, GRID_COLUMNS, GRID_ROWS)   # Draw the grid lines onto our screen
    DrawBorders(borderLines, screen)            # Draw the borders borders onto the screen
    screen.blit(quitText,(20,20))               # Display the textsurface we want to show on the screen
    
    routerSurface.fill((0,0,0,0))               # Clear the routerSurface 
    
    pygame.draw.circle(routerSurface, (AGENT_ROUTER_AREA_TRANSPARENCY), (agent.xPos, agent.yPos), agent.connectionRadius)
    pygame.draw.circle(routerSurface, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.radius)
    pygame.draw.circle(routerSurface, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.connectionRadius, 2)
    
    screen.blit(routerSurface, (0,0))
    
    pygame.display.update()
    fps.tick(60)

def DrawBorders(borderLines,screen):
    for line in borderLines:
        pygame.draw.line(screen,        # Surface to draw to
                        BORDER_COLOUR,  # colour of line
                        ( line.startX , line.startY ),     # Start location of line
                        ( line.endX   , line.endY   ),     # end location of line
                        4)              # Width of line

def FillInsideBorder(borderLines,screen):
    points = [  (borderLines[0].startX, borderLines[0].startY), # Top Left
                (borderLines[0].endX, borderLines[0].endY),     # Top Right
                (borderLines[2].endX, borderLines[2].endY),     # Bottom Right
                (borderLines[2].startX, borderLines[2].startY)] # Bottom Left
    pygame.draw.polygon(
        screen,                 # Screen to draw to
        BORDER_INFILL_COLOUR,   # Colour to graw the polygon with
        points)                 # points of polygon to draw          
    

def DrawGrid(screen, columns, rows):
    horizCellDimension = (WIDTH - (BORDERPADDING * 2)) / columns
    vertiCellDimension = (HEIGHT - (BORDERPADDING * 2)) / rows

    # Draw Vertical Grid Lines
    for x in range(columns - 1):
        x = x + 1
        pygame.draw.line(
            screen,        # Surface  to draw to
            GRID_COLOUR,   # Colour of line
            (BORDERPADDING + (horizCellDimension * x), BORDERPADDING),           # Start location of line
            (BORDERPADDING + (horizCellDimension * x), HEIGHT - BORDERPADDING),  # end location of line
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

if __name__ == '__main__':
    main()