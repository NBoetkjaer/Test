import random
import  pygame as py

BG_COLOR = ( 0, 0, 0) # Baggrunds farve.
cellSize = 10 # Størrelse af et felt i pixels.
gridSize = ( 50, 30 ) # Antal felter på pladen.
screenSize = ( gridSize[0] * cellSize, gridSize[1] * cellSize )
delay = 200

def DrawSnake(): # Funktion til at tegne slangen.
    color = (255, 128, 128) # Slangens farve.
    radius = 0.60 * cellSize
    for pos in snake:
        x = cellSize * pos[0] + cellSize/2
        y = cellSize * pos[1] + cellSize/2
        x = int(x)
        y = int(y)
        py.draw.circle(screen, color, (x, y), int(radius))

def DrawApples(): # Funktion til at tegne æbler.
    color = (0, 255, 0) # Farven på æbler.
    radius = cellSize/2
    for pos in apples:
        x = cellSize * pos[0] + cellSize/2
        y = cellSize * pos[1] + cellSize/2
        x = int(x)
        y = int(y)
        py.draw.circle(screen, color, (x, y), int(radius))

font_name = py.font.match_font('arial')
def draw_text(surf, text, size, x, y): # Funktion til at tegne text på skærmen.
    font = py.font.Font(font_name, size)
    WHITE = 255,255,255
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def AddNewApples(count): # Funktion til at tilføje nye æbler til banen.
    for i in range(0, count):
        x = random.randint(0, gridSize[0] - 1)
        y = random.randint(0, gridSize[1] - 1)
        apples.append( (x,y) )

def HandleMove(dir): # Function til at styre slangen og checke om den skal vokse, dø eller være uændret.
    global delay
    global running

    tmp = snake[0] # Find slanges hoved (første element i listen).
    newHead = (tmp[0] + dir[0], tmp[1] + dir[1]) # Flyt slanges hoved til en ny position. 
    snake.insert(0, newHead ) # Til den nye position af slange hovedet til starten af listen.

    # Check om slangen spiser et æble
    if newHead in apples:
        apples.remove(newHead) # Slet (remove) æblet fra listen af æbler.
        AddNewApples(1) # Tilføj et nyt æble til listen.
        delay -= 5 # Gør spillet lidt hurtigere hver gang slagen har spist et æble.
    else:
        del snake[-1] # Hvis ikke slangen har spist et æble sletter vi halen. PÅ den måde flytter slagen sig.

    # Check for kanibalisme - slangen spiser sig selv.
    if newHead in snake[1:]:
        running = False
    # Check for kollision med kanten af banen.
    if newHead[0] < 0 or newHead[0] >= gridSize[0]:
        running = False
    if newHead[1] < 0 or newHead[1] >= gridSize[1]:
        running = False


py.init() # initialize pygame engine
screen = py.display.set_mode(screenSize) # set screen size.
py.key.set_repeat() # no repeat keys.

direction = (0, 0) # 'direction' er slangens bevægelses retning. Til at starte med står den stille.
# Lav en slange i midten af skærmen. Slangen er en liste af positioner (tuples med to integers x og y)
snake = [(int(gridSize[0]/2), int(gridSize[1]/2))]
# Lav en liste med æbler som slange kan spise.
apples = []
AddNewApples(2) # Indsæt to æbler i listen.

running = True
# Game loop - Spil løkken kører så længe 'running' er sand (True).
while running:
    # Håndtér key inputs.
    allEvents = py.event.get()
    for event in allEvents:
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                direction = (0, -1)
            if event.key == py.K_DOWN:
                direction = (0, 1)
            if event.key == py.K_LEFT:
                direction = (-1, 0)
            if event.key == py.K_RIGHT:
                direction = (1, 0)
            if event.key == py.K_ESCAPE:
                running = False
    
    # Håndtér spil logik (flyt slangen).
    HandleMove(direction)

    # Tegn spillet på skærmen.
    screen.fill(BG_COLOR) # Slet baggrunden - fyld baggrunden med baggrundsfarven.
    DrawApples() # Tegn listen af æbler
    DrawSnake() # Tegn slangen.
    # Tegn point scoren 
    draw_text(screen, 'Point: ' + str(len(snake)),20, screenSize[0]/2, 10)
    py.time.wait(delay) # Hold en kort pause så spillet ikke kører for hurtigt.
    py.display.flip()


py.quit() # Quit pygame.
quit() #Quit python.

