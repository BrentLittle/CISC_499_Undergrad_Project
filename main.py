# DISABLE INITIAL PYGAME CONSOLE PRINT
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# IMPORTS
import sys, pygame
from Border import BorderLine
from AgentRouter import AgentRouter
from FixedRouter import FixedRouter

# INITIALIZE CONSTANTS
WINDOWSIZE = WIDTH, HEIGHT  = (1000,800)
BORDERPADDING               = 50

BACKGROUND_COLOUR       = (200,200,200)
BORDER_COLOUR           = (0,0,0)
BORDER_INFILL_COLOUR    = (255,255,255)
GRID_COLOUR             = (235,235,235)

AGENT_ROUTER_COLOUR             = (204, 0, 0, 255)
AGENT_ROUTER_AREA_TRANSPARENCY  = (255, 128, 128, 128)
FIXED_ROUTER_COLOUR             = (46, 184, 46, 255)
FIXED_ROUTER_AREA_TRANSPARENCY  = (153, 230, 153, 128)

GRID_COLUMNS    = 40
GRID_ROWS       = 32

# Create our display windows and a drawing surface for our routers so they can be semt-transparent on the screen
screen = pygame.display.set_mode( WINDOWSIZE, pygame.NOFRAME )
routerSurface = pygame.Surface( WINDOWSIZE, pygame.SRCALPHA )

def main():
    # Initialize pygame and create window with no frame of a given size
    pygame.init()
    pygame.font.init()
    
    # Initialize Text Surface to display on screen
    myfont = pygame.font.SysFont('arial', 16, True)
    quitText = myfont.render('Press \'ESC\' to Exit', False, (0, 0, 0))
    
    # Fill borderLines in the following order:
    # TOP, RIGHT, BOTTOM, LEFT
            # Left and Right Lines have start at the top and end towards bottom of screen
            # Top and Bottom Lines have start at Left of screen and end towards the Right.
    borderLines = [ BorderLine( BORDERPADDING - 1  , BORDERPADDING         , WIDTH-BORDERPADDING + 1, BORDERPADDING ),
                    BorderLine( WIDTH-BORDERPADDING, BORDERPADDING - 1     , WIDTH-BORDERPADDING    , HEIGHT-BORDERPADDING + 1 ),
                    BorderLine( BORDERPADDING - 1  , HEIGHT - BORDERPADDING, WIDTH-BORDERPADDING + 1, HEIGHT-BORDERPADDING ),
                    BorderLine( BORDERPADDING      , BORDERPADDING - 1     , BORDERPADDING          , HEIGHT-BORDERPADDING + 1 ) ]
    
    agent = AgentRouter(250, 250, 200)
    
    # Fill the background of the windows to our predetermined colour
    screen.fill(BACKGROUND_COLOUR)
    # Fill inside the borders with our backround colour  
    FillInsideBorder(borderLines,screen)
    # Draw the grid lines onto our screen
    DrawGrid(screen, GRID_COLUMNS, GRID_ROWS)
    # Draw the borders borders onto the screen
    DrawBorders(borderLines, screen)
    # Display the textsurface we want to show on the screen
    screen.blit(quitText,(20,20))
    
    #agentSurface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)  # the size of your rect
    #agentSurface.fill(AGENT_ROUTER_AREA_TRANSPARENCY)           # this fills the entire surface
    screen.blit(routerSurface, (0,0))    # (0,0) are the top-left coordinates
    #pygame.draw.circle(screen, (AGENT_ROUTER_AREA_TRANSPARENCY), (agent.xPos, agent.yPos), agent.connectionRadius)
    #pygame.draw.circle(screen, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.radius)
    #pygame.draw.circle(screen, AGENT_ROUTER_COLOUR, (agent.xPos, agent.yPos), agent.connectionRadius, 3)
    
    # Main Loop for Game
    while True:
        for event in pygame.event.get(): 
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        # Update the screen Contents
        Update()
        
        # Render the Screen Contents
        Render()


def Update():
    pygame.display.update()

def Render():
    pygame.display.update()



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