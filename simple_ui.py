import pygame
import sys
import subprocess
import os
from user_management import UserManagement

# Color schemes
COLORS = {
    'primary': (41, 128, 185),      # Blue
    'secondary': (46, 204, 113),    # Green
    'accent': (155, 89, 182),       # Purple
    'warning': (231, 76, 60),       # Red
    'background': (240, 248, 255),  # AliceBlue
    'text': (47, 79, 79),        # DarkSlateGray
    'button': (173, 216, 230),    # LightBlue
    'button_hover': (135, 206, 250), # LightSkyBlue
    'delete': (255, 99, 71),       # Tomato
    'delete_hover': (255, 69, 0),   # OrangeRed
    'success': (60, 179, 113),     # MediumSeaGreen
    'success_hover': (39, 174, 96),  # Darker Green
    'input_bg': (255, 255, 255),   # White
    'input_border': (192, 192, 192), # Silver
    'input_text': (0, 0, 0),         # Black
    'error': (220, 20, 60)         # Crimson
}

# Define Pink colors (matching user_management.py)
PINK = (255, 182, 193)  # LightPink
PINK_HOVER = (255, 105, 180) # HotPink
WHITE = (255, 255, 255)

# Update COLORS dictionary for buttons
COLORS['button'] = PINK
COLORS['button_hover'] = PINK_HOVER

# Ensure assets directory exists
if not os.path.exists('assets'):
    os.makedirs('assets')

# Ensure dataset directory exists
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Check for necessary files and create them if missing
if not os.path.exists('dataset/users.txt'):
    with open('dataset/users.txt', 'w') as f:
        f.write("admin,admin123,admin,ADM001,Admin User,admin@example.com,1234567890\n")

if not os.path.exists('dataset/passwords.txt'):
    with open('dataset/passwords.txt', 'w') as f:
        f.write("admin,admin123\n")

if not os.path.exists('dataset/grades.txt'):
    with open('dataset/grades.txt', 'w') as f:
        pass # Create empty file

if not os.path.exists('dataset/eca.txt'):
    with open('dataset/eca.txt', 'w') as f:
        pass # Create empty file

class BaseUI:
    def __init__(self, width=800, height=600):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Student Management System")
        
        # Set background color
        self.background_color = COLORS['background']
        self.screen.fill(self.background_color)
        
        # Load and scale background image
        try:
            self.bg_image = pygame.image.load('assets/background.png')
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except:
            self.bg_image = None
        
        # Load logo
        try:
            self.logo = pygame.image.load('assets/logo.png')
            self.logo = pygame.transform.scale(self.logo, (150, 150)) # Increased size
        except:
            self.logo = None
        
        # Center the window on the screen
        self.center_window()
        
        # Set up fonts
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.text_font = pygame.font.SysFont('Helvetica', 18)
        self.error_font = pygame.font.SysFont('Helvetica', 14, bold=True)
        
        # Common UI elements
        self.input_width = 400
        self.input_height = 40
        self.input_radius = 10
        self.input_x = (self.width - self.input_width) // 2
        
        self.button_width = 200
        self.button_height = 40
        self.button_radius = 10
        self.button_spacing = 20
    
    def center_window(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        
        # Platform-specific centering
        if sys.platform == 'win32':
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0004)
        else:
            # For other platforms, setting environment variable can work
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
    
    def draw_rounded_rect(self, surface, color, rect, radius, border=0):
        # Draw rounded rectangle with Pygame
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)

    def draw_login_screen(self):
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.background_color)
        
        # Draw logo if available
        if self.logo:
            self.screen.blit(self.logo, ((self.width - 150) // 2, 80))
        
        # Draw title with shadow effect
        title = self.title_font.render("Student Management System", True, COLORS['text'])
        shadow = self.title_font.render("Student Management System", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.width // 2 + 2, 232))
        title_rect = title.get_rect(center=(self.width // 2, 230))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Draw input fields
        username_rect = pygame.Rect(self.input_x, self.username_y, self.input_width, self.input_height)
        password_rect = pygame.Rect(self.input_x, self.password_y, self.input_width, self.input_height)
        
        # Username field
        username_color = COLORS['input_bg'] # Changed to input_bg for consistency
        if self.active_field == 'username':
             username_color = COLORS['button_hover'] # Use hover color when active
        self.draw_rounded_rect(self.screen, username_color, username_rect, self.input_radius)
        self.draw_rounded_rect(self.screen, COLORS['input_border'], username_rect, self.input_radius, 2) # Use input_border
        username_text_surf = self.text_font.render(self.username_text, True, COLORS['input_text']) # Use input_text color
        self.screen.blit(username_text_surf, (self.input_x + 10, self.username_y + 10))
        
        # Password field
        password_color = COLORS['input_bg'] # Changed to input_bg
        if self.active_field == 'password':
            password_color = COLORS['button_hover'] # Use hover color when active
        self.draw_rounded_rect(self.screen, password_color, password_rect, self.input_radius)
        self.draw_rounded_rect(self.screen, COLORS['input_border'], password_rect, self.input_radius, 2) # Use input_border
        password_text_surf = self.text_font.render("*" * len(self.password_text), True, COLORS['input_text']) # Use input_text color
        self.screen.blit(password_text_surf, (self.input_x + 10, self.password_y + 10))
        
        # Labels
        username_label = self.text_font.render("Username:", True, COLORS['text'])
        password_label = self.text_font.render("Password:", True, COLORS['text'])
        self.screen.blit(username_label, (self.input_x, self.username_y - 25))
        self.screen.blit(password_label, (self.input_x, self.password_y - 25))
        
        # Draw Login button
        mouse_pos = pygame.mouse.get_pos()
        login_color = COLORS['button_hover'] if self.login_button_rect.collidepoint(mouse_pos) else COLORS['button']
        self.draw_rounded_rect(self.screen, login_color, self.login_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], self.login_button_rect, self.button_radius, 2) # Border color
        login_text = self.text_font.render("Login", True, WHITE) # Text color to white
        login_text_rect = login_text.get_rect(center=self.login_button_rect.center)
        self.screen.blit(login_text, login_text_rect)
        
        # Draw Exit button
        exit_color = COLORS['delete_hover'] if self.exit_button_rect.collidepoint(mouse_pos) else COLORS['delete']
        self.draw_rounded_rect(self.screen, exit_color, self.exit_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], self.exit_button_rect, self.button_radius, 2) # Border color
        exit_text = self.text_font.render("Exit", True, WHITE) # Text color to white
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)

        # Draw error message if any
        if self.error_message:
            error_text = self.error_font.render(self.error_message, True, COLORS['error'])
            error_rect = error_text.get_rect(center=(self.width // 2, self.login_button_rect.bottom + 30))
            self.screen.blit(error_text, error_rect)

    def handle_login_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active_field:
                if event.key == pygame.K_RETURN:
                    self.login()
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_field == 'username':
                        self.username_text = self.username_text[:-1]
                    elif self.active_field == 'password':
                        self.password_text = self.password_text[:-1]
                elif event.key == pygame.K_TAB:
                    if self.active_field == 'username':
                        self.active_field = 'password'
                    else:
                        self.active_field = 'username'
                else:
                    if self.active_field == 'username':
                        self.username_text += event.unicode
                    elif self.active_field == 'password':
                        self.password_text += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.login_button_rect.collidepoint(event.pos):
                self.login()
            elif self.exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif pygame.Rect(self.input_x, self.username_y, self.input_width, self.input_height).collidepoint(event.pos):
                self.active_field = 'username'
            elif pygame.Rect(self.input_x, self.password_y, self.input_width, self.input_height).collidepoint(event.pos):
                self.active_field = 'password'
            else:
                self.active_field = None

    def login(self):
        try:
            with open('dataset/passwords.txt', 'r') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(',')
                    if stored_username == self.username_text and stored_password == self.password_text:
                        print(f"Login successful for {self.username_text}")
                        pygame.quit() # Quit Pygame before launching the next window
                        UserManagement(self.username_text)
                        return
            self.error_message = "Invalid username or password"
        except FileNotFoundError:
            self.error_message = "Password file not found."
        except Exception as e:
            self.error_message = f"An error occurred: {e}"

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_login_input(event)
            
            self.draw_login_screen()
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()

class MenuUI(BaseUI):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Main Menu - Student Management System")
        
        # Menu buttons
        self.button_rects = {}
        self.create_menu_buttons()
        
        # Run the menu
        self.run_menu()
    
    def create_menu_buttons(self):
        menu_options = ["Login", "Exit"]
        num_buttons = len(menu_options)
        total_height = num_buttons * self.button_height + (num_buttons - 1) * self.button_spacing
        start_y = (self.height - total_height) // 2
        
        current_y = start_y
        for option in menu_options:
            button_rect = pygame.Rect(
                (self.width - self.button_width) // 2,
                current_y,
                self.button_width,
                self.button_height
            )
            self.button_rects[option] = button_rect
            current_y += self.button_height + self.button_spacing
            
    def draw_menu(self):
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.background_color)
            
        # Draw logo
        if self.logo:
             self.screen.blit(self.logo, ((self.width - 150) // 2, 50)) 
             
        # Draw title
        title = self.title_font.render("Main Menu", True, COLORS['text'])
        shadow = self.title_font.render("Main Menu", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.width // 2 + 2, 202))
        title_rect = title.get_rect(center=(self.width // 2, 200))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Draw menu buttons
        mouse_pos = pygame.mouse.get_pos()
        for button_name, rect in self.button_rects.items():
            is_exit = (button_name == "Exit")
            # Use pink for normal buttons, red for exit
            default_color = COLORS['delete'] if is_exit else COLORS['button']
            hover_color = COLORS['delete_hover'] if is_exit else COLORS['button_hover']
            
            color = hover_color if rect.collidepoint(mouse_pos) else default_color
            self.draw_rounded_rect(self.screen, color, rect, self.button_radius)
            self.draw_rounded_rect(self.screen, COLORS['text'], rect, self.button_radius, 2) # Border color
            
            text = self.text_font.render(button_name.replace("_", " ").title(), True, WHITE) # Text color to white
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
    def run_menu(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, rect in self.button_rects.items():
                        if rect.collidepoint(event.pos):
                            if button_name == "Login":
                                running = False
                                LoginUI().run()
                            elif button_name == "Exit":
                                running = False
            
            self.draw_menu()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

class LoginUI(BaseUI):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Login - Student Management System")
        
        # Input fields
        self.username_y = 280
        self.password_y = 350
        self.username_text = ""
        self.password_text = ""
        self.active_field = None
        
        # Login button
        self.login_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.password_y + self.input_height + 30,
            self.button_width,
            self.button_height
        )
        
        # Exit button
        self.exit_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.login_button_rect.bottom + self.button_spacing,
            self.button_width,
            self.button_height
        )
        
        # Error message
        self.error_message = ""

if __name__ == "__main__":
    menu = MenuUI() 