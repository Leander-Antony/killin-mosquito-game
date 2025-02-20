import pygame
import random
import cv2
import mediapipe as mp
import math
import time  # Needed for the timer

# Initialize Pygame
pygame.init()

# Set up the game window in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()

# Load the background image
background_image = pygame.image.load('images/bg.jpg')
background_image = pygame.transform.scale(background_image, (screen_width , screen_height ))

# Load images
mosquito_image = pygame.image.load('images/mosquito.png')
bee_image = pygame.image.load('images/bee.png')
hand_open_image = pygame.image.load('images/hand_open.png')
hand_closed_image = pygame.image.load('images/hand_closed.png')
hand_open_image = pygame.transform.scale(hand_open_image, (150, 150))
hand_closed_image = pygame.transform.scale(hand_closed_image, (150, 150))

hand_image = hand_open_image
hand_rect = hand_image.get_rect(center=(screen_width  // 2, screen_height   // 2))

# Load sounds
pygame.mixer.music.load('sounds/bg.mp3')  # Background music
smack_sound = pygame.mixer.Sound('sounds/smack.mp3')  # Smack sound
damage_sound = pygame.mixer.Sound('sounds/damage.mp3')  # Damage sound (bee)

# Initialize OpenCV and MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Game clock
clock = pygame.time.Clock()

# Mosquito class
class Mosquito:
    def __init__(self):
        self.size = random.randint(20, 60)
        self.image = pygame.transform.scale(mosquito_image, (self.size, self.size))
        self.x = random.randint(0, screen_width  - self.size)
        self.y = random.randint(0, screen_height  - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
        self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
            self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= screen_width  - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= screen_height  - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Bee class
class Bee:
    def __init__(self):
        self.size = random.randint(40, 80)
        self.image = pygame.transform.scale(bee_image, (self.size, self.size))
        self.x = random.randint(0, screen_width  - self.size)
        self.y = random.randint(0, screen_height  - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
            self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= screen_width  - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= screen_height  - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Create mosquito and bee instances
mosquitoes = [Mosquito() for _ in range(10)]
bees = [Bee() for _ in range(3)]

# Calculate distance
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Initialize score
score = 0
font = pygame.font.Font(None, 74)

def start_screen():
    background_color = (20, 20, 20)  # Dark background
    title_color = (255, 215, 0)  # Gold title
    text_color = (200, 200, 200)  # Lighter text
    font_name = "impact.ttf"  # Or any font you have
    title_font_size = 90
    text_font_size = 50
    button_color = (60, 60, 60)
    button_hover_color = (80, 80, 80)

    try:
        title_font = pygame.font.Font(font_name, title_font_size)
        text_font = pygame.font.Font(font_name, text_font_size)
        button_font = pygame.font.Font(font_name, text_font_size)  # Font for buttons
    except pygame.error:
        print(f"Error: Font '{font_name}' not found. Using default font.")
        title_font = pygame.font.Font(None, title_font_size)
        text_font = pygame.font.Font(None, text_font_size)
        button_font = pygame.font.Font(None, text_font_size)

    # Button dimensions and positions
    button_width = 200
    button_height = 50
    start_button_x = screen_width // 2 - button_width // 2
    start_button_y = screen_height // 2 + 50  # Adjust as needed
    quit_button_x = screen_width // 2 - button_width // 2
    quit_button_y = screen_height // 2 + 120  # Adjust as needed

    start_button = pygame.Rect(start_button_x, start_button_y, button_width, button_height)
    quit_button = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)

    start_button_hovered = False
    quit_button_hovered = False

    while True:
        screen.fill(background_color)

        title_text = title_font.render("Mosquito Swatter Game", True, title_color)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 150)) # Adjusted position


        # Draw buttons with hover effect
        start_button_color = button_hover_color if start_button_hovered else button_color
        quit_button_color = button_hover_color if quit_button_hovered else button_color

        pygame.draw.rect(screen, start_button_color, start_button, border_radius=8)  # Rounded corners
        pygame.draw.rect(screen, quit_button_color, quit_button, border_radius=8)  # Rounded corners

        # Button text centered
        start_text = button_font.render("Start", True, text_color)
        screen.blit(start_text, (start_button.x + (button_width - start_text.get_width()) // 2, start_button.y + (button_height - start_text.get_height()) // 2))

        quit_text = button_font.render("Quit", True, text_color)
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEMOTION:  # For hover effect
                mouse_pos = pygame.mouse.get_pos()
                start_button_hovered = start_button.collidepoint(mouse_pos)
                quit_button_hovered = quit_button.collidepoint(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False
# Timer function
def game_timer():
    return time.time()

def game():
    global score
    score = 0
    start_time = game_timer()
    total_game_time = 30  # Game duration in seconds
    
    # Play background music
    pygame.mixer.music.play(-1)  # Loop background music
    
    # Initialize hand_image to default open hand at the start
    hand_image = hand_open_image

    running = True
    while running:
        # Check timer (30 seconds)
        elapsed_time = time.time() - start_time
        remaining_time = total_game_time - elapsed_time
        if remaining_time <= 0:
            break

        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x9, y9 = hand_landmarks.landmark[9].x * screen_width, hand_landmarks.landmark[9].y * 800
                x12, y12 = hand_landmarks.landmark[12].x * screen_width, hand_landmarks.landmark[12].y * 800

                distance_9_12 = calculate_distance((x9, y9), (x12, y12))
                if distance_9_12 < 50:
                    hand_image = hand_closed_image
                    for mosquito in mosquitoes[:]:
                        if hand_rect.colliderect(pygame.Rect(mosquito.x, mosquito.y, mosquito.size, mosquito.size)):
                            mosquitoes.remove(mosquito)
                            mosquitoes.append(Mosquito())
                            score += 1
                            smack_sound.play()  # Play smack sound when mosquito is hit
                    for bee in bees[:]:
                        if hand_rect.colliderect(pygame.Rect(bee.x, bee.y, bee.size, bee.size)):
                            bees.remove(bee)
                            bees.append(Bee())
                            score -= 3
                            damage_sound.play()  # Play damage sound when bee is hit
                else:
                    hand_image = hand_open_image

                x8 = (1 - hand_landmarks.landmark[8].x) * screen_width 
                y8 = hand_landmarks.landmark[8].y * screen_height 
                hand_rect.center = (x8, y8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))
        screen.blit(hand_image, hand_rect)

        for mosquito in mosquitoes:
            mosquito.move()
            mosquito.draw(screen)

        for bee in bees:
            bee.move()
            bee.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # Display remaining time
        timer_text = font.render(f"Time: {int(remaining_time)}s", True, (255, 255, 255))
        screen.blit(timer_text, (screen.get_width() - 200, 20))

        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()  # Stop background music when game ends
    return score

# End screen
def end_screen(final_score):
    background_color = (20, 20, 20)  # Dark background
    title_color = (255, 215, 0)  # Gold title
    text_color = (200, 200, 200)  # Lighter text
    font_name = "impact.ttf"  # Or any font you have
    title_font_size = 80
    text_font_size = 50

    try:
        title_font = pygame.font.Font(font_name, title_font_size)
        text_font = pygame.font.Font(font_name, text_font_size)
    except pygame.error:
        print(f"Error: Font '{font_name}' not found. Using default font.")
        title_font = pygame.font.Font(None, title_font_size)
        text_font = pygame.font.Font(None, text_font_size)


    while True:
        screen.fill(background_color)  # Dark background

        title_text = title_font.render(f"Game Over!", True, title_color)
        score_text = title_font.render(f"Final Score: {final_score}", True, title_color) # Gold score
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 250))

        instruction_text = text_font.render("Press SPACE to Play Again or Q to Quit", True, text_color)
        screen.blit(instruction_text, (screen.get_width() // 2 - instruction_text.get_width() // 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False

# Main game loop
while True:
    if not start_screen():
        break
    final_score = game()
    if not end_screen(final_score):
        break

pygame.quit()
