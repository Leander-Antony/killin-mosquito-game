import pygame
import random
import cv2
import mediapipe as mp
import math
import time  # Needed for the timer

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1200, 800))

# Load the background image
background_image = pygame.image.load('images/bg.jpg')
background_image = pygame.transform.scale(background_image, (1200, 800))

# Load images
mosquito_image = pygame.image.load('images/mosquito.png')
bee_image = pygame.image.load('images/bee.png')
hand_open_image = pygame.image.load('images/hand_open.png')
hand_closed_image = pygame.image.load('images/hand_closed.png')
hand_open_image = pygame.transform.scale(hand_open_image, (150, 150))
hand_closed_image = pygame.transform.scale(hand_closed_image, (150, 150))

hand_image = hand_open_image
hand_rect = hand_image.get_rect(center=(1200 // 2, 800 // 2))

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
        self.x = random.randint(0, 1200 - self.size)
        self.y = random.randint(0, 800 - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
        self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
            self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= 1200 - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= 800 - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Bee class
class Bee:
    def __init__(self):
        self.size = random.randint(40, 80)
        self.image = pygame.transform.scale(bee_image, (self.size, self.size))
        self.x = random.randint(0, 1200 - self.size)
        self.y = random.randint(0, 800 - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
            self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= 1200 - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= 800 - self.size:
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

# Start screen function
def start_screen():
    screen.fill((0, 0, 0))
    title_font = pygame.font.Font(None, 100)
    title_text = title_font.render("Mosquito Swatter Game", True, (255, 255, 255))
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 200))

    start_font = pygame.font.Font(None, 74)
    start_text = start_font.render("Press SPACE to Start or Q to Quit", True, (255, 255, 255))
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 400))

    pygame.display.update()

    while True:
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
                x9, y9 = hand_landmarks.landmark[9].x * 1200, hand_landmarks.landmark[9].y * 800
                x12, y12 = hand_landmarks.landmark[12].x * 1200, hand_landmarks.landmark[12].y * 800

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

                x8 = (1 - hand_landmarks.landmark[8].x) * 1200
                y8 = hand_landmarks.landmark[8].y * 800
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
    screen.fill((0, 0, 0))
    end_font = pygame.font.Font(None, 100)
    end_text = end_font.render(f"Game Over! Final Score: {final_score}", True, (255, 255, 255))
    screen.blit(end_text, (screen.get_width() // 2 - end_text.get_width() // 2, 200))

    start_font = pygame.font.Font(None, 74)
    start_text = start_font.render("Press SPACE to Play Again or Q to Quit", True, (255, 255, 255))
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 400))

    pygame.display.update()

    while True:
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
