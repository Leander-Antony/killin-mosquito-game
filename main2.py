import pygame
import random
import cv2
import mediapipe as mp
import math
import time
import sys
import tkinter as tk
from tkinter import messagebox


# Initialize Pygame
pygame.init()

# Set up the game window in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()

# Load the background image
background_image = pygame.image.load('images/bg.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load images (adjusted for full-screen resolution)
mosquito_image = pygame.image.load('images/mosquito.png')
bee_image = pygame.image.load('images/bee.png')
hand_open_image_p1 = pygame.image.load('images/hand_open.png')  
hand_closed_image_p1 = pygame.image.load('images/hand_closed.png')  
hand_open_image_p2 = pygame.image.load('images/hand_open.png')  
hand_closed_image_p2 = pygame.image.load('images/hand_closed.png')  

hand_open_image_p1 = pygame.transform.scale(hand_open_image_p1, (150, 150))
hand_closed_image_p1 = pygame.transform.scale(hand_closed_image_p1, (150, 150))
hand_open_image_p2 = pygame.transform.scale(hand_open_image_p2, (150, 150))
hand_closed_image_p2 = pygame.transform.scale(hand_closed_image_p2, (150, 150))
hand_open_image_p2.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_ADD)  
hand_closed_image_p2 = hand_closed_image_p1.copy()
hand_closed_image_p2.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_ADD)

# Load sounds
pygame.mixer.music.load('sounds/bg.mp3')
smack_sound = pygame.mixer.Sound('sounds/smack.mp3')
damage_sound = pygame.mixer.Sound('sounds/damage.mp3')
nooo_sound = pygame.mixer.Sound('sounds/nooo.mp3')

# Initialize OpenCV and MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Game clock
clock = pygame.time.Clock()

# Mosquito class
class Mosquito:
    def __init__(self):
        self.size = random.randint(20, 60)
        self.image = pygame.transform.scale(mosquito_image, (self.size, self.size))
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
        self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)
            self.speed_y = random.choice([-1, 1]) * random.randint(2, 5)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= screen_width - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= screen_height - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Bee class
class Bee:
    def __init__(self):
        self.size = random.randint(40, 80)
        self.image = pygame.transform.scale(bee_image, (self.size, self.size))
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)

    def move(self):
        if random.randint(0, 100) < 5:
            self.speed_x = random.choice([-1, 1]) * random.randint(1, 4)
            self.speed_y = random.choice([-1, 1]) * random.randint(1, 4)
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= screen_width - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= screen_height - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Create mosquito and bee instances
mosquitoes = [Mosquito() for _ in range(10)]
bees = [Bee() for _ in range(3)]

# Calculate distance
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Initialize scores
score_p1 = 0
score_p2 = 0
font = pygame.font.Font(None, 74)

# Timer function
def game_timer():
    return time.time()

# Load power-up image
power_up_image = pygame.image.load('images/power_up.png')
power_up_image = pygame.transform.scale(power_up_image, (100, 100))  # Adjust size if needed

# Power-up class
class PowerUp:
    def __init__(self):
        self.image = power_up_image
        self.x = random.randint(0, screen_width - 100)
        self.y = random.randint(0, screen_height - 100)
        self.active = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def reset_position(self):
        self.x = random.randint(0, screen_width - 100)
        self.y = random.randint(0, screen_height - 100)
        self.active = True

# Initialize power-up and timer
power_up = PowerUp()
power_up_spawn_time = time.time()




# Assuming screen, screen_width, and screen_height are already initialized
def start_screen(): 

    # Button dimensions and colors
    button_color = (50, 200, 50)
    quit_button_color = (200, 50, 50)
    button_width, button_height = 200, 80
    button_font = pygame.font.Font(None, 60)

    # Start button rect
    start_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 100), (button_width, button_height))
    quit_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 200), (button_width, button_height))

    # Main screen loop
    while True:
        screen.blit(background_image, (0, 0))  # Draw background image

        # Title
        title_font = pygame.font.Font(None, 100)
        text = title_font.render("Welcome to the Swat Game!", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() - 100))

        # Draw buttons
        pygame.draw.rect(screen, button_color, start_button)
        pygame.draw.rect(screen, quit_button_color, quit_button)

        # Start button text
        start_text = button_font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (start_button.x + (button_width - start_text.get_width()) // 2, start_button.y + (button_height - start_text.get_height()) // 2))

        # Quit button text
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return  # Exit this function to start the game
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()




# End screen function
def end_screen(winner, score_p1, score_p2):
    # Button dimensions and colors
    restart_button_color = (50, 200, 50)
    quit_button_color = (200, 50, 50)
    button_width, button_height = 200, 80
    button_font = pygame.font.Font(None, 60)

    # Button rectangles
    restart_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 100), (button_width, button_height))
    quit_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 200), (button_width, button_height))

    while True:
        screen.blit(background_image, (0, 0))  # Draw background image

        # Display winner and scores
        title_font = pygame.font.Font(None, 100)
        winner_text = title_font.render(f"{winner} wins!", True, (255, 255, 255))
        screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() - 100))

        score_font = pygame.font.Font(None, 74)
        score_text = score_font.render(f"Player 1: {score_p1} | Player 2: {score_p2}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))

        # Draw buttons
        pygame.draw.rect(screen, restart_button_color, restart_button)
        pygame.draw.rect(screen, quit_button_color, quit_button)

        # Restart button text
        restart_text = button_font.render("Restart", True, (255, 255, 255))
        screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2, restart_button.y + (button_height - restart_text.get_height()) // 2))

        # Quit button text
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


def game():
    global score_p1, score_p2, power_up_spawn_time
    score_p1 = 0
    score_p2 = 0
    start_time = game_timer()
    total_game_time = 30  # Game duration in seconds

    # Play background music
    pygame.mixer.music.play(-1)  # Loop background music

    running = True
    while running:
        # Check timer (30 seconds)
        elapsed_time = time.time() - start_time
        remaining_time = total_game_time - elapsed_time
        if remaining_time <= 0:
            break

        # Spawn power-up every 10 seconds
        if time.time() - power_up_spawn_time >= 10:
            power_up.reset_position()
            power_up_spawn_time = time.time()

        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        # First, draw background and elements like mosquitoes and bees
        screen.blit(background_image, (0, 0))

        # Draw mosquitoes and bees
        for mosquito in mosquitoes:
            mosquito.move()
            mosquito.draw(screen)
        for bee in bees:
            bee.move()
            bee.draw(screen)

        # Draw power-up
        power_up.draw(screen)

        # Draw scores
        score_text_p1 = font.render(f"Player 1 Score: {score_p1}", True, (255, 255, 255))
        score_text_p2 = font.render(f"Player 2 Score: {score_p2}", True, (255, 255, 255))
        screen.blit(score_text_p1, (50, 50))
        screen.blit(score_text_p2, (50, 150))

        # Draw remaining time
        timer_text = font.render(f"Time: {int(remaining_time)}s", True, (255, 0, 0))
        screen.blit(timer_text, (1000, 50))

        if result.multi_hand_landmarks:
            # Iterate through hands for both players
            for hand_landmarks, hand_index in zip(result.multi_hand_landmarks, range(len(result.multi_hand_landmarks))):
                if hand_index == 0:
                    hand_image = hand_open_image_p1
                    x9, y9 = hand_landmarks.landmark[9].x * screen_width, hand_landmarks.landmark[9].y * screen_height
                    x12, y12 = hand_landmarks.landmark[12].x * screen_width, hand_landmarks.landmark[12].y * screen_height
                    x8 = (1 - hand_landmarks.landmark[8].x) * screen_width
                    y8 = hand_landmarks.landmark[8].y * screen_height
                    distance_9_12 = calculate_distance((x9, y9), (x12, y12))

                    if distance_9_12 < 50:
                        hand_image = hand_closed_image_p1
                        for mosquito in mosquitoes[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(mosquito.x, mosquito.y, mosquito.size, mosquito.size)):
                                mosquitoes.remove(mosquito)
                                mosquitoes.append(Mosquito())
                                score_p1 += 1
                                smack_sound.play()
                        for bee in bees[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(bee.x, bee.y, bee.size, bee.size)):
                                bees.remove(bee)
                                bees.append(Bee())
                                score_p1 -= 3
                                damage_sound.play()

                        # Player 1 collects power-up
                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(power_up.x, power_up.y, 100, 100)) and power_up.active:
                            score_p1 += 10
                            power_up.active = False  # Deactivate power-up once collected

                    screen.blit(hand_image, (x8, y8))

                elif hand_index == 1:
                    hand_image = hand_open_image_p2
                    x9, y9 = (1 - hand_landmarks.landmark[9].x) * screen_width, hand_landmarks.landmark[9].y * screen_height
                    x12, y12 = (1 - hand_landmarks.landmark[12].x) * screen_width, hand_landmarks.landmark[12].y * screen_height
                    x8 = (1 - hand_landmarks.landmark[8].x) * screen_width
                    y8 = hand_landmarks.landmark[8].y * screen_height
                    distance_9_12 = calculate_distance((x9, y9), (x12, y12))

                    if distance_9_12 < 50:
                        hand_image = hand_closed_image_p2
                        for mosquito in mosquitoes[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(mosquito.x, mosquito.y, mosquito.size, mosquito.size)):
                                mosquitoes.remove(mosquito)
                                mosquitoes.append(Mosquito())
                                score_p2 += 1
                                smack_sound.play()
                        for bee in bees[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(bee.x, bee.y, bee.size, bee.size)):
                                bees.remove(bee)
                                bees.append(Bee())
                                score_p2 -= 3
                                damage_sound.play()

                        # Player 2 collects power-up
                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(power_up.x, power_up.y, 100, 100)) and power_up.active:
                            score_p2 += 10
                            power_up.active = False  # Deactivate power-up once collected

                    screen.blit(hand_image, (x8, y8))

        # Update the display
        pygame.display.update()
        clock.tick(30)

    # End the game and stop music
    pygame.mixer.music.stop()
    # Determine the winner
    if score_p1 > score_p2:
        winner = "Player 1"
    elif score_p2 > score_p1:
        winner = "Player 2"
    else:
        winner = "No one"
    return winner, score_p1, score_p2 # Return winner and scores
   





# Main game loop
while True:
    start_screen()
    winner, score_p1, score_p2 = game() # Get winner and scores from game()
    if end_screen(winner, score_p1, score_p2): # If restart is clicked
        continue # Start the game loop again
    else: # If quit is clicked
        break 

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()