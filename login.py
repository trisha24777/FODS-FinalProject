import pygame
import sys
import os

class LoginUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Login - Student Management System")
        
        # Set white background
        self.background_color = (255, 255, 255)
        self.screen.fill(self.background_color)
        
        # Center the window on the screen
        self.center_window()
        
        # Set up fonts
        self.title_font = pygame.font.SysFont('Helvetica', 24, bold=True)
        self.text_font = pygame.font.SysFont('Helvetica', 16)
        self.input_font = pygame.font.SysFont('Helvetica', 14)
        
        # Create text surfaces
        self.title_text = self.title_font.render("Login", True, (0, 0, 0))
        
        # Input fields
        self.username = ""
        self.password = ""
        self.active_field = None
        
        # Create input boxes
        self.input_box_width = 300
        self.input_box_height = 30
        self.input_box_radius = 5  # Border radius for input boxes
        self.username_box = pygame.Rect((self.width - self.input_box_width) // 2, 150, 
                                   self.input_box_width, self.input_box_height)
        self.password_box = pygame.Rect((self.width - self.input_box_width) // 2, 200, 
                                      self.input_box_width, self.input_box_height)
        
        # Buttons
        self.button_width = 300
        self.button_height = 40
        self.button_spacing = 20
        self.button_radius = 10  # Border radius for buttons
        
        # Login button
        self.login_button_y = 280
        self.login_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.login_button_y,
            self.button_width,
            self.button_height
        )
        
        # Back button
        self.back_button_y = self.login_button_y + self.button_height + self.button_spacing
        self.back_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.back_button_y,
            self.button_width,
            self.button_height
        )
        
        # Colors
        self.button_color = (200, 200, 200)
        self.button_hover_color = (180, 180, 180)
        self.active_box_color = (220, 220, 220)
        self.inactive_box_color = (240, 240, 240)
        
        # Error message
        self.error_message = ""
        self.error_color = (255, 0, 0)
        
        # Run the main loop
        self.run()
    
    def center_window(self):
        # Get screen info
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        
        # Calculate position for center of screen
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        
        # Set window position (this is platform-dependent)
        if sys.platform == 'win32':
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
        # Note: Centering on macOS and Linux may require different approaches
    
    def draw_rounded_rect(self, surface, color, rect, radius, border=0):
        """Draw a rounded rectangle with optional border"""
        # Draw the main rectangle
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
    
    def validate_credentials(self):
        # Simple validation - replace with your actual validation logic
        # For now, we'll check against the dataset/passwords.txt file
        try:
            with open('dataset/passwords.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    if username == self.username and password == self.password:
                        return True
            return False
        except FileNotFoundError:
            print("Passwords file not found")
            return False
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if username box was clicked
                    if self.username_box.collidepoint(mouse_pos):
                        self.active_field = "username"
                    # Check if password box was clicked
                    elif self.password_box.collidepoint(mouse_pos):
                        self.active_field = "password"
                    # Check if login button was clicked
                    elif self.login_button_rect.collidepoint(mouse_pos):
                        if self.validate_credentials():
                            print("Login successful!")
                            # Launch user management interface
                            running = False
                            pygame.quit()
                            from user_management import UserManagement
                            UserManagement(self.username)
                        else:
                            self.error_message = "Invalid username or password"
                    # Check if back button was clicked
                    elif self.back_button_rect.collidepoint(mouse_pos):
                        # Return to the main menu
                        running = False
                        pygame.quit()
                        from simple_ui import MenuUI
                        MenuUI()
                    else:
                        self.active_field = None
                
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    if self.active_field:
                        if event.key == pygame.K_RETURN:
                            if self.active_field == "username":
                                self.active_field = "password"
                            elif self.active_field == "password":
                                if self.validate_credentials():
                                    print("Login successful!")
                                    running = False
                                    pygame.quit()
                                    from user_management import UserManagement
                                    UserManagement(self.username)
                                else:
                                    self.error_message = "Invalid username or password"
                        elif event.key == pygame.K_BACKSPACE:
                            if self.active_field == "username":
                                self.username = self.username[:-1]
                            else:
                                self.password = self.password[:-1]
                        elif event.key == pygame.K_TAB:
                            if self.active_field == "username":
                                self.active_field = "password"
                            else:
                                self.active_field = "username"
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            pygame.quit()
                            from simple_ui import MenuUI
                            MenuUI()
                        else:
                            if self.active_field == "username":
                                self.username += event.unicode
                            else:
                                self.password += event.unicode
            
            # Clear the screen with white background
            self.screen.fill(self.background_color)
            
            # Draw title
            title_rect = self.title_text.get_rect(center=(self.width // 2, 80))
            self.screen.blit(self.title_text, title_rect)
            
            # Draw username label
            username_label = self.text_font.render("Username:", True, (0, 0, 0))
            username_label_rect = username_label.get_rect(right=self.username_box.left - 10, 
                                                  centery=self.username_box.centery)
            self.screen.blit(username_label, username_label_rect)
            
            # Draw password label
            password_label = self.text_font.render("Password:", True, (0, 0, 0))
            password_label_rect = password_label.get_rect(right=self.password_box.left - 10,
                                                        centery=self.password_box.centery)
            self.screen.blit(password_label, password_label_rect)
            
            # Draw input boxes
            username_color = self.active_box_color if self.active_field == "username" else self.inactive_box_color
            password_color = self.active_box_color if self.active_field == "password" else self.inactive_box_color
            
            self.draw_rounded_rect(self.screen, username_color, self.username_box, self.input_box_radius)
            self.draw_rounded_rect(self.screen, (0, 0, 0), self.username_box, self.input_box_radius, 2)
            
            self.draw_rounded_rect(self.screen, password_color, self.password_box, self.input_box_radius)
            self.draw_rounded_rect(self.screen, (0, 0, 0), self.password_box, self.input_box_radius, 2)
            
            # Draw input text
            username_surface = self.input_font.render(self.username, True, (0, 0, 0))
            self.screen.blit(username_surface, (self.username_box.x + 5, self.username_box.y + 5))
            
            # Draw password as asterisks
            password_display = "*" * len(self.password)
            password_surface = self.input_font.render(password_display, True, (0, 0, 0))
            self.screen.blit(password_surface, (self.password_box.x + 5, self.password_box.y + 5))
            
            # Draw error message if any
            if self.error_message:
                error_surface = self.text_font.render(self.error_message, True, self.error_color)
                error_rect = error_surface.get_rect(center=(self.width // 2, 250))
                self.screen.blit(error_surface, error_rect)
            
            # Get mouse position for hover effects
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw login button
            login_color = self.button_hover_color if self.login_button_rect.collidepoint(mouse_pos) else self.button_color
            self.draw_rounded_rect(self.screen, login_color, self.login_button_rect, self.button_radius)
            self.draw_rounded_rect(self.screen, (0, 0, 0), self.login_button_rect, self.button_radius, 2)
            
            login_text = self.text_font.render("Login", True, (0, 0, 0))
            login_text_rect = login_text.get_rect(center=self.login_button_rect.center)
            self.screen.blit(login_text, login_text_rect)
            
            # Draw back button
            back_color = self.button_hover_color if self.back_button_rect.collidepoint(mouse_pos) else self.button_color
            self.draw_rounded_rect(self.screen, back_color, self.back_button_rect, self.button_radius)
            self.draw_rounded_rect(self.screen, (0, 0, 0), self.back_button_rect, self.button_radius, 2)
            
            back_text = self.text_font.render("Back to Menu", True, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
            self.screen.blit(back_text, back_text_rect)
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(60)
        
        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = LoginUI() 