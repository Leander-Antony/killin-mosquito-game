import pygame
import random
import cv2
import mediapipe as mp
import math
import time
import sys

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

class Mosquito:
    def __init__(self):
        self.size = random.randint(20, 60)
        self.image = pygame.transform.scale(mosquito_image, (self.size, self.size))
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.base_speed = random.randint(2, 5)  # Initialize base_speed HERE
        self.speed_x = random.choice([-1, 1]) * self.base_speed # Use base_speed here
        self.speed_y = random.choice([-1, 1]) * self.base_speed # Use base_speed here
        self.change_direction_frequency = 5  # Initial frequency (lower is more frequent)

    def move(self, difficulty):  # Add difficulty parameter
        speed_multiplier = 1 + difficulty * 0.8  # Adjust speed based on difficulty
        current_speed_x = self.base_speed * speed_multiplier
        current_speed_y = self.base_speed * speed_multiplier

        if random.randint(0, 100) < self.change_direction_frequency:  # Changed to variable
            self.speed_x = random.choice([-1, 1]) * current_speed_x
            self.speed_y = random.choice([-1, 1]) * current_speed_y

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
        self.base_speed = random.randint(1, 4)  # Initialize base_speed HERE
        self.speed_x = random.choice([-1, 1]) * self.base_speed # Use base_speed here
        self.speed_y = random.choice([-1, 1]) * self.base_speed # Use base_speed here
        self.change_direction_frequency = 8  # Initial frequency

    def move(self, difficulty): # Add difficulty parameter
        speed_multiplier = 1 + difficulty * 0.5  # Adjust speed based on difficulty
        current_speed_x = self.base_speed * speed_multiplier
        current_speed_y = self.base_speed * speed_multiplier
        if random.randint(0, 100) < self.change_direction_frequency: # Changed to variable
            self.speed_x = random.choice([-1, 1]) * current_speed_x
            self.speed_y = random.choice([-1, 1]) * current_speed_y
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= screen_width - self.size:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= screen_height - self.size:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))



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

# Power-up classes (including Mega Swat)
class PowerUp:
    def __init__(self, image):  # Add image parameter
        self.image = image
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

class MegaSwat(PowerUp):  # MegaSwat inherits from PowerUp
    def __init__(self, image):
        super().__init__(image)  # Call the parent's __init__
        self.swatted = False  # Track if Mega Swat has been used

# Load Mega Swat image
mega_swat_image = pygame.image.load('images/boom.png') # Make sure this path is correct
mega_swat_image = pygame.transform.scale(mega_swat_image, (100, 100))

# Initialize power-ups
power_up = PowerUp(power_up_image)  # Normal power-up
mega_swat = MegaSwat(mega_swat_image) # Mega Swat power-up
power_up_spawn_time = time.time()
mega_swat_spawn_time = time.time()





def start_screen():
    background_color = (20, 20, 20)
    title_color = (255, 215, 0)  # Gold
    button_color = (60, 60, 60)
    button_hover_color = (80, 80, 80)
    text_color = (255, 255, 255)
    font_name = "impact.ttf" # Or any font you have
    title_font_size = 90
    button_font_size = 40
    button_width, button_height = 250, 60
    button_margin = 20

    try:
        title_font = pygame.font.Font(font_name, title_font_size)
        button_font = pygame.font.Font(font_name, button_font_size)
    except pygame.error:
        print(f"Error: Font '{font_name}' not found. Using default font.")
        title_font = pygame.font.Font(None, title_font_size)
        button_font = pygame.font.Font(None, button_font_size)


    try:
        screen_width = int(screen.get_width())  # Get actual screen dimensions
        screen_height = int(screen.get_height())
    except AttributeError: # in case screen has not been initialized yet
        screen_width = 800
        screen_height = 600
        print("Screen not yet initialized. Using default values.")


    total_button_width = (button_width * 2) + button_margin
    buttons_x = (screen_width - total_button_width) // 2
    start_button_x = buttons_x
    quit_button_x = buttons_x + button_width + button_margin
    buttons_y = screen_height // 2 + 150

    start_button = pygame.Rect(start_button_x, buttons_y, button_width, button_height)
    quit_button = pygame.Rect(quit_button_x, buttons_y, button_width, button_height)

    start_button_hovered = False
    quit_button_hovered = False

    while True:
        screen.fill(background_color)

        title_text = title_font.render("Welcome to the Swat Game!", True, title_color)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - title_text.get_height() - 50))

        # Buttons with hover and rounded corners
        start_button_color = button_hover_color if start_button_hovered else button_color
        quit_button_color = button_hover_color if quit_button_hovered else button_color

        pygame.draw.rect(screen, start_button_color, start_button, border_radius=8)
        pygame.draw.rect(screen, quit_button_color, quit_button, border_radius=8)

        start_text = button_font.render("Start", True, text_color)
        screen.blit(start_text, (start_button.x + (button_width - start_text.get_width()) // 2, start_button.y + (button_height - start_text.get_height()) // 2))

        quit_text = button_font.render("Quit", True, text_color)
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                start_button_hovered = start_button.collidepoint(mouse_pos)
                quit_button_hovered = quit_button.collidepoint(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return  # Start the game
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()





def end_screen(winner, score_p1, score_p2):
    # Colors and styles
    background_color = (20, 20, 20)  # Darker background
    title_color = (255, 215, 0)  # Gold title
    score_color = (200, 200, 200)  # Lighter score
    button_color = (60, 60, 60)  # Darker buttons
    button_hover_color = (80, 80, 80) # Hover color
    text_color = (255, 255, 255)
    font_name = "impact.ttf" # Example, replace with your font file or system font
    title_font_size = 80
    score_font_size = 50
    button_font_size = 40
    button_width, button_height = 250, 60
    button_margin = 20  # Space between buttons

    try:
        title_font = pygame.font.Font(font_name, title_font_size)
        score_font = pygame.font.Font(font_name, score_font_size)
        button_font = pygame.font.Font(font_name, button_font_size)
    except pygame.error:
        print(f"Error: Font '{font_name}' not found. Using default font.")
        title_font = pygame.font.Font(None, title_font_size)
        score_font = pygame.font.Font(None, score_font_size)
        button_font = pygame.font.Font(None, button_font_size)

    # Calculate button positions with margin
    total_button_width = (button_width * 2) + button_margin
    buttons_x = (screen_width - total_button_width) // 2
    restart_button_x = buttons_x
    quit_button_x = buttons_x + button_width + button_margin
    buttons_y = screen_height // 2 + 150 # Adjust vertical position

    restart_button = pygame.Rect(restart_button_x, buttons_y, button_width, button_height)
    quit_button = pygame.Rect(quit_button_x, buttons_y, button_width, button_height)

    restart_button_hovered = False
    quit_button_hovered = False


    while True:
        screen.fill(background_color)  # Fill with dark background

        # Display winner and scores
        winner_text = title_font.render(f"{winner} wins!", True, title_color)
        screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() - 50))  # Adjusted position

        score_text = score_font.render(f"Player 1: {score_p1} | Player 2: {score_p2}", True, score_color)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 20)) # Adjusted position


        # Draw buttons with hover effect
        restart_button_color = button_hover_color if restart_button_hovered else button_color
        quit_button_color = button_hover_color if quit_button_hovered else button_color

        pygame.draw.rect(screen, restart_button_color, restart_button, border_radius=8) # Rounded corners
        pygame.draw.rect(screen, quit_button_color, quit_button, border_radius=8) # Rounded corners

        # Button text centered
        restart_text = button_font.render("Restart", True, text_color)
        screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2, restart_button.y + (button_height - restart_text.get_height()) // 2))

        quit_text = button_font.render("Quit", True, text_color)
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                restart_button_hovered = restart_button.collidepoint(mouse_pos)
                quit_button_hovered = quit_button.collidepoint(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


def game():
    global score_p1, score_p2, power_up_spawn_time, mega_swat_spawn_time
    score_p1 = 0
    score_p2 = 0
    start_time = game_timer()
    total_game_time = 30  # Game duration in seconds
    score_history_p1 = []  # Keep track of recent scores for P1
    score_history_p2 = []  # Keep track of recent scores for P2
    difficulty_p1 = 0  # Initialize difficulty level for P1
    difficulty_p2 = 0  # Initialize difficulty level for P2
    mosquitoes = [Mosquito() for _ in range(10)]  # Initialize mosquitoes here
    bees = [Bee() for _ in range(3)]  # Initialize bees here

    # Play background music with smoother transition
    pygame.mixer.music.play(-1)  # Loop background music
    score_font = pygame.font.Font("impact.ttf", 60) # Or any font you have
    timer_font = pygame.font.Font("impact.ttf", 40) # Or any font you have

    running = True
    while running:
        # Check timer (30 seconds)
        elapsed_time = time.time() - start_time
        remaining_time = total_game_time - elapsed_time
        if remaining_time <= 0:
            break

        # Spawn power-ups
        if time.time() - power_up_spawn_time >= 10:
            power_up.reset_position()
            power_up_spawn_time = time.time()

        if time.time() - mega_swat_spawn_time >= 20: # Mega Swat spawns less frequently
            mega_swat.reset_position()
            mega_swat_spawn_time = time.time()
            mega_swat.swatted = False # Reset the swatted status

        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        # First, draw background and elements like mosquitoes and bees
        screen.blit(background_image, (0, 0))


            

            
            

        # Draw power-up with highlight when active
        # Draw power-ups
        if power_up.active:
            power_up.draw(screen)

        if mega_swat.active:
            mega_swat.draw(screen)

        # --- Score Display ---
        score_text_p1 = score_font.render(f"P1: {score_p1}", True, (0, 255, 0))  # Green
        score_text_p2 = score_font.render(f"P2: {score_p2}", True, (0, 0, 255))  # Blue
    

        # Calculate Difficulty (Moved BEFORE the hand tracking loop)
        if result.multi_hand_landmarks: # Check if hands are detected before calculating difficulty
            for hand_landmarks, hand_index in zip(result.multi_hand_landmarks, range(len(result.multi_hand_landmarks))):
                if hand_index == 0:
                    difficulty_p1 = calculate_difficulty(score_history_p1)
                elif hand_index == 1:
                    difficulty_p2 = calculate_difficulty(score_history_p2)

        for mosquito in mosquitoes:
            # Now, difficulty_p1 and difficulty_p2 are available
            mosquito.move(difficulty_p1)
            mosquito.draw(screen)  # If only one player is needed, change this to difficulty_p1
        for bee in bees:
            bee.move(difficulty_p1)
            bee.draw(screen) # If only one player is needed, change this to difficulty_p1


        # Positions (adjust as needed)
        score_p1_x = 50
        score_p1_y = 50
        score_p2_x = screen_width - score_text_p2.get_width() - 50  # Right side
        score_p2_y = 50

        screen.blit(score_text_p1, (score_p1_x, score_p1_y))
        screen.blit(score_text_p2, (score_p2_x, score_p2_y))

        # --- Timer Display (Progress Bar and Text) ---
        progress_bar_width = 300  # Reduced width
        progress_bar_height = 20
        time_bar_length = (remaining_time / total_game_time) * progress_bar_width

        # Position (centered at the top)
        progress_bar_x = (screen_width - progress_bar_width) // 2
        progress_bar_y = 20

        # Draw progress bar background
        pygame.draw.rect(screen, (50, 50, 50), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))  # Dark gray background
        # Draw progress bar
        pygame.draw.rect(screen, (255, 0, 0), (progress_bar_x, progress_bar_y, time_bar_length, progress_bar_height))  # Red

        # Timer Text (below the bar, centered)
        timer_text = timer_font.render(f"Time: {int(remaining_time)}s", True, (255, 255, 255))
        timer_text_x = (screen_width - timer_text.get_width()) // 2
        timer_text_y = progress_bar_y + progress_bar_height + 10  # Below the bar

        screen.blit(timer_text, (timer_text_x, timer_text_y))


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
                                score_history_p1.append(score_p1)
                                smack_sound.play()
                        for bee in bees[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(bee.x, bee.y, bee.size, bee.size)):
                                bees.remove(bee)
                                bees.append(Bee())
                                score_p1 -= 3
                                score_history_p1.append(score_p1)
                                damage_sound.play()

                        # Player 1 collects power-up
                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(power_up.x, power_up.y, 100, 100)) and power_up.active:
                            score_p1 += 10
                            power_up.active = False  
                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(mega_swat.x, mega_swat.y, 100, 100)) and mega_swat.active and not mega_swat.swatted:
                            score_p1 += 25 # Add all mosquito sizes to the score
                            mosquitoes.clear() # Remove all mosquitoes
                            mosquitoes.extend([Mosquito() for _ in range(10)]) # Respawn mosquitoes
                            mega_swat.active = False
                            mega_swat.swatted = True
                            smack_sound.play()


                    hand_image.set_alpha(200)  
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
                                score_history_p1.append(score_p2)
                                smack_sound.play()
                        for bee in bees[:]:
                            if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(bee.x, bee.y, bee.size, bee.size)):
                                bees.remove(bee)
                                bees.append(Bee())
                                score_p2 -= 3
                                score_history_p1.append(score_p2)
                                damage_sound.play()

                        # Player 2 collects power-up
                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(power_up.x, power_up.y, 100, 100)) and power_up.active:
                            score_p2 += 10
                            power_up.active = False  # Deactivate power-up once collected

                        if pygame.Rect(x8, y8, 150, 150).colliderect(pygame.Rect(mega_swat.x, mega_swat.y, 100, 100)) and mega_swat.active and not mega_swat.swatted:
                            score_p2 += 25 # Add all mosquito sizes to the score
                            mosquitoes.clear() # Remove all mosquitoes
                            mosquitoes.extend([Mosquito() for _ in range(10)]) # Respawn mosquitoes
                            mega_swat.active = False
                            mega_swat.swatted = True
                            smack_sound.play()

                    # Add transparency to hand images
                    hand_image.set_alpha(200)  # Set hand transparency
                    screen.blit(hand_image, (x8, y8))

        # Update the display
        pygame.display.update()
        clock.tick(30)

    # End the game and stop music
    pygame.mixer.music.stop()

    if score_p1 > score_p2:
        winner = "Player 1"
    elif score_p2 > score_p1:
        winner = "Player 2"
    else:
        winner = "No one"
    return winner, score_p1, score_p2

def calculate_difficulty(score_history):
    if not score_history:
        return 0  # Start at difficulty 0

    average_score = sum(score_history[-5:]) / min(len(score_history), 5)  # Average of last 5, or all if less than 5
    if average_score < 5:
        return 0
    elif average_score < 15:
        return 1
    else:
        return 2

# Main game loop
while True:
    start_screen()
    winner, score_p1, score_p2 = game() 
    if end_screen(winner, score_p1, score_p2): 
        continue 
    else: 
        break 

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()