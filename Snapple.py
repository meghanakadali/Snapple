import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BRIGHT_RADIOACTIVE_GREEN = (57, 255, 20)  # Bright radioactive green color for the snake
BRIGHT_RED = (255, 0, 0)
BRIGHT_YELLOW = (255, 255, 0)
BRIGHT_BLUE = (0, 191, 255)
BROWN = (128, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Display settings
display_width = 1000
display_height = 600
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake Game")

# Load and scale images
bg_intro = pygame.transform.scale(pygame.image.load("intro.jpg"), (display_width, display_height))
bg_pause = pygame.transform.scale(pygame.image.load("pause.jpg"), (display_width, display_height))
bg_gameover = pygame.transform.scale(pygame.image.load("end.jpg"), (display_width, display_height))
bg_game = pygame.transform.scale(pygame.image.load("simple.jpg"), (display_width, display_height))

# Load sounds
eat_sound = pygame.mixer.Sound("sound.wav")
game_over_sound = pygame.mixer.Sound("sound2.wav")

# Fonts
smallfont = pygame.font.SysFont("comicsansms", 30)
medfont = pygame.font.SysFont("Helvetica", 50)
largefont = pygame.font.SysFont("Helvetica", 80)

# Clock
clock = pygame.time.Clock()

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width // 2, (display_height // 2) + y_displace)  # Center horizontally
    window.blit(textSurf, textRect)

def game_intro():
    """Display the game intro screen."""
    intro = True
    while intro:
        window.fill(BLACK)
        window.blit(bg_intro, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Aesthetically styled intro text with bright colors
        message_to_screen("SNAPPLE!", BRIGHT_RED, -160, "large")
        message_to_screen("Eat red apples to grow!", BLACK, -80)
        message_to_screen("Avoid hitting yourself or the edges!", BLACK, -40)
        message_to_screen("Press P to Play | Q to Quit", BLACK, 40)

        pygame.display.update()
        clock.tick(15)

def pause():
    """Pause the game."""
    paused = True
    while paused:
        window.fill(BLACK)
        window.blit(bg_pause, (0, 0))
        message_to_screen("Game Paused!", BRIGHT_RED, -160, "large")
        message_to_screen("Press Y to Continue | Press Q to Quit", WHITE, -50, "medium")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_y:
                    paused = False

def game_over(score):
    """Display game over screen and ask to replay or quit."""
    window.fill(BLACK)
    window.blit(bg_gameover, (0, 0))
    message_to_screen("Game Over!", BRIGHT_RED, -160, "large")
    message_to_screen(f"Score: {score}", WHITE, -70, "medium")
    message_to_screen("Press R to Replay | Q to Quit", WHITE, 50, "medium")
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()  # Restart the game

class Snake:
    """Snake class to handle movement and collision."""
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"

    def changeDirTo(self, dir):
        if dir == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10

        self.body.insert(0, list(self.position))

        if self.position == foodPos:
            return 1  # Ate food
        else:
            self.body.pop()
            return 0

    def checkCollision(self):
        """Check if the snake collides with itself or the wall."""
        if self.position[0] >= display_width or self.position[0] < 0 or self.position[1] >= display_height or self.position[1] < 0:
            game_over_sound.play()
            return True
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                game_over_sound.play()
                return True
        return False

class FoodSpawner:
    """Handles food spawning."""
    def __init__(self):
        self.position = [random.randrange(1, display_width // 10) * 10, random.randrange(1, display_height // 10) * 10]
        self.isFoodOnScreen = True

    def spawnFood(self):
        """Spawn food in a random position."""
        if not self.isFoodOnScreen:
            self.position = [random.randrange(1, display_width // 10) * 10, random.randrange(1, display_height // 10) * 10]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, status):
        self.isFoodOnScreen = status

def main_game():
    """Main game loop."""
    snake = Snake()
    foodSpawner = FoodSpawner()
    score = 0

    # Initial game speed
    speed = 15  # Starting speed
    speed_increase_threshold = 5  # Increase speed every 5 points

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.changeDirTo('RIGHT')
                if event.key == pygame.K_UP:
                    snake.changeDirTo('UP')
                if event.key == pygame.K_DOWN:
                    snake.changeDirTo('DOWN')
                if event.key == pygame.K_LEFT:
                    snake.changeDirTo('LEFT')
                if event.key == pygame.K_p:
                    pause()

        # Move snake
        foodPos = foodSpawner.spawnFood()
        if snake.move(foodPos) == 1:
            score += 1
            eat_sound.play()
            foodSpawner.setFoodOnScreen(False)

            # Increase speed every few points
            if score % speed_increase_threshold == 0:
                speed += 1  # Increase speed

        # Check for collisions
        if snake.checkCollision():
            game_over(score)
            return  # Exit the main game loop

        # Update screen
        window.fill(BLACK)
        window.blit(bg_game, (0, 0))

        # Draw snake with bright radioactive color
        for pos in snake.body:
            pygame.draw.rect(window, BRIGHT_RADIOACTIVE_GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food
        pygame.draw.rect(window, RED, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

        pygame.display.set_caption(f"Snake Game | Score: {score}")
        pygame.display.flip()
        clock.tick(speed)  # Use the adjusted speed here

# Start the game
game_intro()
main_game()

pygame.quit()
