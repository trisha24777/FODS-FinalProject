import pygame
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

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

# New color definitions
PINK = (255, 182, 193)  # LightPink
PINK_HOVER = (255, 105, 180) # HotPink
WHITE = (255, 255, 255)

# Update COLORS dictionary
COLORS['button'] = PINK
COLORS['button_hover'] = PINK_HOVER

# Convert RGB tuples to matplotlib color format
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Create matplotlib color dictionary
MPL_COLORS = {k: rgb_to_hex(v) for k, v in COLORS.items()}

class DataDisplayWindow:
    def __init__(self, data, display_type, is_admin=False, parent_window=None):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Data Display - Student Management System")
        
        # Set background
        self.background_color = COLORS['background']
        self.screen.fill(self.background_color)
        
        # Load and scale background image
        try:
            self.bg_image = pygame.image.load('assets/background.png')
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except:
            self.bg_image = None
        
        # Center the window
        self.center_window()
        
        # Set up fonts
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.text_font = pygame.font.SysFont('Helvetica', 16)
        self.label_font = pygame.font.SysFont('Helvetica', 14) # Smaller font for labels
        
        # Store data and parent window
        self.data = data
        self.display_type = display_type
        self.is_admin = is_admin
        self.parent_window = parent_window
        
        # Create title text
        titles = {
            "marks": "Student Marks",
            "eca": "ECA Activities",
            "achievements": "Student Achievements",
            "students": "All Students",
            "visualization": "Marks Visualization"
        }
        self.title_text = titles[display_type]
        self.title_surface = self.title_font.render(self.title_text, True, COLORS['text'])
        
        # Create visualization buttons if needed
        self.viz_buttons = {}
        if display_type == "visualization":
            # For marks visualization
            if isinstance(data, pygame.Surface) and hasattr(parent_window, 'visualize_marks'):
                # Center the buttons
                button_width = 150
                button_height = 30
                button_spacing = 20
                total_width = 4 * button_width + 3 * button_spacing
                start_x = (self.width - total_width) // 2
                
                self.viz_buttons = {
                    'student_avg': pygame.Rect(start_x, 100, button_width, button_height),
                    'subject_perf': pygame.Rect(start_x + button_width + button_spacing, 100, button_width, button_height),
                    'grade_dist': pygame.Rect(start_x + 2 * (button_width + button_spacing), 100, button_width, button_height),
                    'subject_dist': pygame.Rect(start_x + 3 * (button_width + button_spacing), 100, button_width, button_height)
                }
                
                # Remove subject-specific buttons
                if not hasattr(parent_window, 'current_marks_viz'):
                    parent_window.current_marks_viz = 'student_avg'
            
            # For ECA visualization - no buttons needed, just show the pie chart
            elif isinstance(data, pygame.Surface) and hasattr(parent_window, 'visualize_eca'):
                # No buttons for ECA visualization
                pass
        
        # Back button
        self.button_width = 200
        self.button_height = 40
        self.button_radius = 10
        self.back_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.height - 80,
            self.button_width,
            self.button_height
        )
        
        # Run the window
        self.run()
    
    def center_window(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        if sys.platform == 'win32':
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0x0001)
    
    def draw_rounded_rect(self, surface, color, rect, radius, border=0):
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
    
    def draw_data(self):
        # Draw background image if available
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.background_color)
        
        # Draw title with shadow effect
        shadow_text = self.title_font.render(self.title_text, True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 2, 52))
        self.screen.blit(shadow_text, shadow_rect)
        
        title_rect = self.title_surface.get_rect(center=(self.width // 2, 50))
        self.screen.blit(self.title_surface, title_rect)
        
        # Draw visualization buttons if needed
        if self.viz_buttons:
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw buttons for marks visualization
            if self.display_type == "visualization" and hasattr(self.parent_window, 'visualize_marks'):
                button_labels = {
                    'student_avg': "Student Averages",
                    'subject_perf': "Subject Performance",
                    'grade_dist': "Grade Distribution",
                    'subject_dist': "Subject Distribution"
                }
                
                for key, rect in self.viz_buttons.items():
                    color = COLORS['button_hover'] if rect.collidepoint(mouse_pos) else COLORS['button']
                    if self.parent_window.current_marks_viz == key:
                        color = COLORS['success']
                    
                    self.draw_rounded_rect(self.screen, color, rect, 5)
                    self.draw_rounded_rect(self.screen, COLORS['text'], rect, 5, 2)
                    
                    text = self.text_font.render(button_labels.get(key, key), True, WHITE)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                
                # Draw the smaller, centered graph
                graph_x = (self.width - self.data.get_width()) // 2
                graph_y = 140 # Position below buttons
                self.screen.blit(self.data, (graph_x, graph_y))
            
            # For ECA visualization - just draw the pie chart without buttons
            elif self.display_type == "visualization" and hasattr(self.parent_window, 'visualize_eca'):
                # Move graph higher (from y=150 to y=120)
                self.screen.blit(self.data, (50, 120))
        
        # Draw data content with a semi-transparent panel
        elif self.display_type != "visualization":
            panel = pygame.Surface((self.width - 100, self.height - 200))
            panel.fill(COLORS['background'])
            panel.set_alpha(230)
            self.screen.blit(panel, (50, 100))
            
            y_offset = 120
            if self.display_type == "marks":
                # For admin, show student selection buttons
                if self.is_admin:
                    # Get unique usernames from marks data
                    usernames = sorted(set(username for username, _, _ in self.data))
                    
                    # Create buttons for each student
                    button_width = 200
                    button_height = 30
                    button_spacing = 10
                    buttons_per_row = 3
                    
                    # Draw student selection buttons
                    for i, username in enumerate(usernames):
                        row = i // buttons_per_row
                        col = i % buttons_per_row
                        
                        button_rect = pygame.Rect(
                            70 + col * (button_width + button_spacing),
                            y_offset + row * (button_height + button_spacing),
                            button_width,
                            button_height
                        )
                        
                        # Store button rect for click detection
                        if not hasattr(self, 'student_buttons'):
                            self.student_buttons = {}
                        self.student_buttons[username] = button_rect
                        
                        # Highlight selected student
                        color = COLORS['success'] if hasattr(self, 'selected_student') and self.selected_student == username else COLORS['button']
                        if button_rect.collidepoint(pygame.mouse.get_pos()):
                            color = COLORS['button_hover']
                        
                        self.draw_rounded_rect(self.screen, color, button_rect, 5)
                        self.draw_rounded_rect(self.screen, COLORS['text'], button_rect, 5, 2)
                        
                        text = self.text_font.render(username, True, WHITE)
                        text_rect = text.get_rect(center=button_rect.center)
                        self.screen.blit(text, text_rect)
                    
                    # Update y_offset for marks display
                    y_offset += (len(usernames) // buttons_per_row + 1) * (button_height + button_spacing) + 20
                    
                    # Show marks for selected student or all students if none selected
                    if hasattr(self, 'selected_student') and self.selected_student:
                        # Filter marks for selected student
                        student_marks = [(u, s, g) for u, s, g in self.data if u == self.selected_student]
                        for username, subject, grade in student_marks:
                            text = self.text_font.render(f"{subject}: {grade}", True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
                    else:
                        # Show all marks
                        for username, subject, grade in self.data:
                            text = self.text_font.render(f"{username} - {subject}: {grade}", True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
                else:
                    # Student view - show only their marks
                    for data in self.data:
                        # Fix for student view - check if data has 2 or 3 elements
                        if len(data) == 3:
                            username, subject, grade = data
                            # Only show if it's the current student's data
                            if username == self.parent_window.username:
                                text = self.text_font.render(f"{subject}: {grade}", True, COLORS['text'])
                                self.screen.blit(text, (70, y_offset))
                                y_offset += 30
                        elif len(data) == 2:
                            subject, grade = data
                            text = self.text_font.render(f"{subject}: {grade}", True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
            elif self.display_type == "eca":
                # For admin, show student selection buttons
                if self.is_admin:
                    # Get unique usernames from ECA data
                    usernames = sorted(set(username for username, _ in self.data))
                    
                    # Create buttons for each student
                    button_width = 200
                    button_height = 30
                    button_spacing = 10
                    buttons_per_row = 3
                    
                    # Draw student selection buttons
                    for i, username in enumerate(usernames):
                        row = i // buttons_per_row
                        col = i % buttons_per_row
                        
                        button_rect = pygame.Rect(
                            70 + col * (button_width + button_spacing),
                            y_offset + row * (button_height + button_spacing),
                            button_width,
                            button_height
                        )
                        
                        # Store button rect for click detection
                        if not hasattr(self, 'student_buttons'):
                            self.student_buttons = {}
                        self.student_buttons[username] = button_rect
                        
                        # Highlight selected student
                        color = COLORS['success'] if hasattr(self, 'selected_student') and self.selected_student == username else COLORS['button']
                        if button_rect.collidepoint(pygame.mouse.get_pos()):
                            color = COLORS['button_hover']
                        
                        self.draw_rounded_rect(self.screen, color, button_rect, 5)
                        self.draw_rounded_rect(self.screen, COLORS['text'], button_rect, 5, 2)
                        
                        text = self.text_font.render(username, True, WHITE)
                        text_rect = text.get_rect(center=button_rect.center)
                        self.screen.blit(text, text_rect)
                    
                    # Update y_offset for ECA display
                    y_offset += (len(usernames) // buttons_per_row + 1) * (button_height + button_spacing) + 20
                    
                    # Show ECA for selected student or all students if none selected
                    if hasattr(self, 'selected_student') and self.selected_student:
                        # Filter ECA for selected student
                        student_eca = [(u, a) for u, a in self.data if u == self.selected_student]
                        for username, activity in student_eca:
                            text = self.text_font.render(activity, True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
                    else:
                        # Show all ECA
                        for username, activity in self.data:
                            text = self.text_font.render(f"{username} - {activity}", True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
                else:
                    # Student view - show only their ECA
                    for data in self.data:
                        # Fix for student view - check if data has 1 or 2 elements
                        if len(data) == 2:
                            username, activity = data
                            # Only show if it's the current student's data
                            if username == self.parent_window.username:
                                text = self.text_font.render(activity, True, COLORS['text'])
                                self.screen.blit(text, (70, y_offset))
                                y_offset += 30
                        elif len(data) == 1:
                            activity = data[0]
                            text = self.text_font.render(activity, True, COLORS['text'])
                            self.screen.blit(text, (70, y_offset))
                            y_offset += 30
            elif self.display_type == "students":
                for username, name, email, phone in self.data:
                    # Display name, username, email, and phone
                    display_text = f"{name} ({username}) - {email} - {phone}"
                    text = self.text_font.render(display_text, True, COLORS['text'])
                    self.screen.blit(text, (70, y_offset))
                    y_offset += 30
        
        # Draw back button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        back_color = COLORS['button_hover'] if self.back_button_rect.collidepoint(mouse_pos) else COLORS['button']
        self.draw_rounded_rect(self.screen, back_color, self.back_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], self.back_button_rect, self.button_radius, 2)
        
        back_text = self.text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Handle visualization button clicks
                    if self.viz_buttons:
                        for key, rect in self.viz_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                if hasattr(self.parent_window, 'visualize_marks'):
                                    self.parent_window.current_marks_viz = key
                                    self.data = self.parent_window.visualize_marks()
                                # No need to handle ECA visualization buttons as they're removed
                    
                    # Handle student selection buttons for marks and ECA
                    if hasattr(self, 'student_buttons'):
                        for username, rect in self.student_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                self.selected_student = username
                                break
                    
                    # Handle back button click
                    if self.back_button_rect.collidepoint(mouse_pos):
                        running = False
                        if self.parent_window:
                            self.parent_window.run()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        if self.parent_window:
                            self.parent_window.run()
            
            # Draw data
            self.draw_data()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

class UserManagement:
    def __init__(self, username):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("User Management - Student Management System")
        
        # Set background
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
            self.logo = pygame.transform.scale(self.logo, (100, 100))
        except:
            self.logo = None
        
        # Center the window
        self.center_window()
        
        # Set up fonts
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.text_font = pygame.font.SysFont('Helvetica', 16)
        self.label_font = pygame.font.SysFont('Helvetica', 14) # Smaller font for labels
        
        # Store username and check if admin
        self.username = username
        self.is_admin = self.check_if_admin()
        
        # Create text surfaces
        self.title_text = f"Welcome, {'Admin ' if self.is_admin else ''}{username}!"
        self.title_surface = self.title_font.render(self.title_text, True, COLORS['text'])
        
        # Buttons
        self.button_width = 300
        self.button_height = 40
        self.button_spacing = 20
        self.button_radius = 10
        
        # Initialize button positions
        self.current_y = 180
        
        # Admin buttons
        if self.is_admin:
            self.add_student_button_rect = self.create_button("Add Student")
            self.current_y += self.button_height + self.button_spacing
            
            self.delete_student_button_rect = self.create_button("Delete Student")
            self.current_y += self.button_height + self.button_spacing
            
            self.view_students_button_rect = self.create_button("View All Students")
            self.current_y += self.button_height + self.button_spacing
            
            self.visualize_marks_button_rect = self.create_button("Visualize Marks")
            self.current_y += self.button_height + self.button_spacing
        
        # View Marks button
        self.marks_button_rect = self.create_button("View Marks")
        self.current_y += self.button_height + self.button_spacing
        
        # View ECA button
        self.eca_button_rect = self.create_button("View ECA Activities")
        self.current_y += self.button_height + self.button_spacing
        
        # Logout button
        self.logout_button_rect = self.create_button("Logout")
        self.current_y += self.button_height + self.button_spacing # Add spacing after logout button
        
        # Back button (to return to main menu) - positioned explicitly at the bottom center
        self.back_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,  # Center horizontally
            self.height - 60,  # Bottom position
            self.button_width,
            self.button_height
        )
        
        # Input fields for adding student
        self.input_fields = {}
        self.active_field = None
        self.new_student_data = {
            "username": "",
            "password": "",
            "name": "",
            "email": "",
            "phone": "",
            "marks_math": "",
            "marks_science": "",
            "marks_english": "",
            "marks_history": "",
            "marks_computer": "",
            "eca": "",
        }
        
        # Delete student mode
        self.showing_delete_student = False
        self.students_to_delete = []
        self.selected_student = None
        
        # Run the main loop
        self.run()
    
    def create_button(self, text):
        button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.current_y,
            self.button_width,
            self.button_height
        )
        return button_rect
    
    def check_if_admin(self):
        try:
            with open('dataset/users.txt', 'r') as file:
                for line in file:
                    username, password, role, *_ = line.strip().split(',')
                    if username == self.username and role == 'admin':
                        return True
            return False
        except FileNotFoundError:
            return False
    
    def center_window(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        if sys.platform == 'win32':
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0x0001)
    
    def draw_rounded_rect(self, surface, color, rect, radius, border=0):
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
    
    def load_marks(self):
        try:
            marks = []
            with open('dataset/grades.txt', 'r') as file:
                for line in file:
                    username, subject, grade = line.strip().split(',')
                    if username == self.username or self.is_admin:
                        marks.append((username, subject, grade))
            return marks
        except FileNotFoundError:
            return []
    
    def load_eca(self):
        try:
            activities = []
            with open('dataset/eca.txt', 'r') as file:
                for line in file:
                    username, activity = line.strip().split(',')
                    if username == self.username or self.is_admin:
                        activities.append((username, activity))
            return activities
        except FileNotFoundError:
            return []
    
    def load_all_students(self):
        try:
            students = []
            with open('dataset/users.txt', 'r') as file:
                for line_num, line in enumerate(file):
                    line = line.strip()
                    if not line: # Skip empty lines
                        continue
                    parts = line.split(',')
                    # Expecting: username, password, role, id, name, email, phone
                    if len(parts) == 7:
                        username, password, role, user_id, name, email, phone = parts
                        if role == 'student':
                            students.append((username, name, email, phone))
                    else:
                        print(f"Warning: Skipping malformed line {line_num + 1} in users.txt: {line}")
            return students
        except FileNotFoundError:
            print("Warning: users.txt not found.")
            return []
        except Exception as e:
            print(f"Error loading students: {e}")
            return []
    
    def add_student(self):
        # Validate input fields
        username = self.new_student_data['username'].strip()
        password = self.new_student_data['password'].strip()
        name = self.new_student_data['name'].strip()
        email = self.new_student_data['email'].strip()
        phone = self.new_student_data['phone'].strip()
        role = 'student'
        
        # Extract marks data
        marks_math = self.new_student_data['marks_math'].strip()
        marks_science = self.new_student_data['marks_science'].strip()
        marks_english = self.new_student_data['marks_english'].strip()
        marks_history = self.new_student_data['marks_history'].strip()
        marks_computer = self.new_student_data['marks_computer'].strip()
        
        # Extract ECA data
        eca = self.new_student_data['eca'].strip()
        
        # Validate required basic information
        if not all([username, password, name, email, phone]):
            self.error_message = "All basic information fields are required."
            return False
            
        # Basic email validation
        if '@' not in email or '.' not in email:
            self.error_message = "Invalid email format."
            return False
            
        # Basic phone validation (digits only)
        if not phone.isdigit():
             self.error_message = "Phone number must contain only digits."
             return False
             
        # Validate marks (if provided)
        marks_fields = [marks_math, marks_science, marks_english, marks_history, marks_computer]
        subjects = ["Mathematics", "Science", "English", "History", "Computer Science"]
        
        for i, mark in enumerate(marks_fields):
            if mark and not mark.isdigit():
                self.error_message = f"Invalid {subjects[i]} mark. Please enter a numeric value."
                return False
            # Validate mark is within reasonable range if provided
            if mark and (int(mark) < 0 or int(mark) > 100):
                self.error_message = f"{subjects[i]} mark should be between 0 and 100."
                return False

        # Check if username already exists
        try:
            with open('dataset/users.txt', 'r') as f:
                for line in f:
                    if line.startswith(username + ','):
                        self.error_message = f"Username '{username}' already exists."
                        return False
        except FileNotFoundError:
            pass # File doesn't exist, so username can't exist yet

        # Generate user ID (example: STU001)
        user_id_prefix = "STU"
        next_id = 1
        try:
            with open('dataset/users.txt', 'r') as f:
                 existing_ids = [line.split(',')[2] for line in f if line.strip() and len(line.split(',')) > 2]
                 stu_ids = [int(id[len(user_id_prefix):]) for id in existing_ids if id.startswith(user_id_prefix) and id[len(user_id_prefix):].isdigit()]
                 if stu_ids:
                    next_id = max(stu_ids) + 1
        except FileNotFoundError:
            pass # Start with ID 1 if file doesn't exist
            
        user_id = f"{user_id_prefix}{next_id:03d}"
        
        # Append new user to users.txt
        user_data_line = f"{username},password,student,{user_id},{name},{email},{phone}\n" # Note: Storing plain password temporarily
        try:
            with open('dataset/users.txt', 'a') as f:
                f.write(user_data_line)
        except IOError as e:
            self.error_message = f"Error writing to users file: {e}"
            return False
            
        # Append new user to passwords.txt
        password_line = f"{username},{password}\n"
        try:
            with open('dataset/passwords.txt', 'a') as f:
                f.write(password_line)
        except IOError as e:
             self.error_message = f"Error writing to passwords file: {e}"
             # Attempt to clean up the entry in users.txt if password writing failed
             try:
                 with open('dataset/users.txt', 'r') as f:
                     lines = f.readlines()
                 with open('dataset/users.txt', 'w') as f:
                     for line in lines:
                         if not line.startswith(username + ','):
                             f.write(line)
             except Exception as cleanup_e:
                 print(f"Error during cleanup: {cleanup_e}")
             return False
        
        # Add marks to grades.txt if provided
        try:
            with open('dataset/grades.txt', 'a') as f:
                for i, mark in enumerate(marks_fields):
                    if mark:  # Only add if mark is provided
                        grade_line = f"{username},{subjects[i]},{mark}\n"
                        f.write(grade_line)
        except IOError as e:
            self.error_message = f"Error writing to grades file: {e}"
            # We don't delete the user at this point, just report the error
            print(f"Warning: User created but grades not saved: {e}")
        
        # Add ECA activities to eca.txt if provided
        if eca:
            try:
                # Handle multiple activities separated by semicolons or commas
                activities = [a.strip() for a in eca.replace(';', ',').split(',') if a.strip()]
                
                with open('dataset/eca.txt', 'a') as f:
                    for activity in activities:
                        eca_line = f"{username},{activity}\n"
                        f.write(eca_line)
            except IOError as e:
                self.error_message = f"Error writing to ECA file: {e}"
                # We don't delete the user at this point, just report the error
                print(f"Warning: User created but ECA not saved: {e}")

        print(f"Student '{name}' ({username}) added successfully with ID {user_id}.")
        self.error_message = "" # Clear error on success
        return True
    
    def visualize_marks(self):
        # Create a figure with a single plot and higher DPI
        fig = plt.figure(figsize=(12, 8), dpi=150)
        fig.patch.set_facecolor(MPL_COLORS['background'])  # Match background color
        
        # Get marks data
        marks = self.load_marks()
        
        # Prepare data for different visualizations
        student_marks = {}
        subject_marks = {}
        
        for username, subject, grade in marks:
            # For student averages
            if username not in student_marks:
                student_marks[username] = []
            student_marks[username].append(float(grade))
            
            # For subject averages
            if subject not in subject_marks:
                subject_marks[subject] = []
            subject_marks[subject].append(float(grade))
        
        # Create a single large plot
        ax = fig.add_subplot(111)
        
        # Determine which visualization to show based on the current selection
        if not hasattr(self, 'current_marks_viz'):
            self.current_marks_viz = 'student_avg'
        
        if self.current_marks_viz == 'student_avg':
            # Bar chart for student averages
            students = list(student_marks.keys())
            averages = [sum(marks)/len(marks) for marks in student_marks.values()]
            
            bars = ax.bar(students, averages, color=MPL_COLORS['primary'])
            ax.set_title('Average Marks by Student', pad=20, color=MPL_COLORS['text'], fontsize=16)
            ax.set_xlabel('Student', color=MPL_COLORS['text'], fontsize=14)
            ax.set_ylabel('Average Grade', color=MPL_COLORS['text'], fontsize=14)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom')
        
        elif self.current_marks_viz == 'subject_perf':
            # Line chart for subject performance
            subjects = list(subject_marks.keys())
            subject_averages = [sum(marks)/len(marks) for marks in subject_marks.values()]
            
            ax.plot(subjects, subject_averages, marker='o', color=MPL_COLORS['secondary'], linewidth=2)
            ax.set_title('Subject-wise Performance', pad=20, color=MPL_COLORS['text'], fontsize=16)
            ax.set_xlabel('Subject', color=MPL_COLORS['text'], fontsize=14)
            ax.set_ylabel('Average Grade', color=MPL_COLORS['text'], fontsize=14)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Add value labels on points
            for i, value in enumerate(subject_averages):
                ax.text(i, value, f'{value:.1f}', ha='center', va='bottom')
        
        elif self.current_marks_viz == 'grade_dist':
            # Pie chart for grade distribution
            grade_ranges = {
                'A (90-100)': 0,
                'B (80-89)': 0,
                'C (70-79)': 0,
                'D (60-69)': 0,
                'F (<60)': 0
            }
            
            for grades in student_marks.values():
                for grade in grades:
                    if grade >= 90:
                        grade_ranges['A (90-100)'] += 1
                    elif grade >= 80:
                        grade_ranges['B (80-89)'] += 1
                    elif grade >= 70:
                        grade_ranges['C (70-79)'] += 1
                    elif grade >= 60:
                        grade_ranges['D (60-69)'] += 1
                    else:
                        grade_ranges['F (<60)'] += 1
            
            colors = [MPL_COLORS['success'], MPL_COLORS['primary'], MPL_COLORS['button'], MPL_COLORS['accent'], MPL_COLORS['warning']]
            wedges, texts, autotexts = ax.pie(grade_ranges.values(), labels=grade_ranges.keys(), autopct='%1.1f%%',
                                          colors=colors, startangle=90)
            ax.set_title('Grade Distribution', pad=20, color=MPL_COLORS['text'], fontsize=16)
        
        elif self.current_marks_viz == 'subject_dist':
            # Box plot for grade distribution by subject
            subjects = list(subject_marks.keys())
            subject_data = [subject_marks[subject] for subject in subjects]
            box = ax.boxplot(subject_data, labels=subjects, patch_artist=True)
            
            # Customize box plot colors
            for patch in box['boxes']:
                patch.set_facecolor(MPL_COLORS['primary'])
            
            ax.set_title('Grade Distribution by Subject', pad=20, color=MPL_COLORS['text'], fontsize=16)
            ax.set_xlabel('Subject', color=MPL_COLORS['text'], fontsize=14)
            ax.set_ylabel('Grade', color=MPL_COLORS['text'], fontsize=14)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Adjust layout and style
        plt.tight_layout()
        fig.patch.set_facecolor(MPL_COLORS['background'])
        
        # Convert to Pygame surface
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        
        # Scale the surface to a smaller size using smoothscale
        target_width = self.width - 200  # Reduced from -100
        target_height = self.height - 250 # Reduced from -200
        scaled_surf = pygame.transform.smoothscale(surf, (target_width, target_height))
        
        return scaled_surf
    
    def visualize_eca(self):
        # Create a figure with a single plot and higher DPI
        fig = plt.figure(figsize=(16, 10), dpi=150)
        fig.patch.set_facecolor(MPL_COLORS['background'])
        
        # Get ECA data
        activities = self.load_eca()
        
        # Prepare data for visualizations
        activity_counts = {}
        student_activities = {}
        activity_types = {
            'Sports': ['Football', 'Basketball', 'Cricket', 'Tennis'],
            'Arts': ['Drama', 'Music', 'Dance', 'Art'],
            'Academic': ['Debate', 'Science Club', 'Math Club'],
            'Other': ['Community Service', 'Environmental Club']
        }
        
        for username, activity in activities:
            # Count activities
            if activity not in activity_counts:
                activity_counts[activity] = 0
            activity_counts[activity] += 1
            
            # Group by student
            if username not in student_activities:
                student_activities[username] = set()
            student_activities[username].add(activity)
        
        # Create a single large plot with proper margins
        ax = fig.add_subplot(111)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        
        # Always show activity distribution (pie chart)
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(activity_counts)))
        wedges, texts, autotexts = ax.pie(activity_counts.values(), labels=activity_counts.keys(), autopct='%1.1f%%',
                                      colors=colors, startangle=90, textprops={'fontsize': 12})
        ax.set_title('ECA Activity Distribution', pad=20, color=MPL_COLORS['text'], fontsize=20)
        
        # Adjust layout and style
        plt.tight_layout()
        
        # Convert to Pygame surface with higher quality
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        
        # Scale the surface to fit the window while maintaining aspect ratio
        target_width = self.width - 100
        target_height = self.height - 200
        scaled_surf = pygame.transform.smoothscale(surf, (target_width, target_height))
        
        return scaled_surf
    
    def draw_add_student_form(self):
        # Define input fields and positions
        basic_fields = ["username", "password", "name", "email", "phone"]
        marks_fields = ["marks_math", "marks_science", "marks_english", "marks_history", "marks_computer"]
        eca_fields = ["eca"]
        
        # Define layout parameters
        input_height = 40
        input_spacing_v = 60  # Increased from 50
        input_width = 300     # Reduced from 320 
        
        # Draw title
        title = self.title_font.render("Add New Student", True, COLORS['text'])
        title_rect = title.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title, title_rect)
        
        input_rects = {}
        
        # Calculate column positions with more spacing between columns
        left_col_x = self.width // 4 - input_width // 2 - 20  # Move left column more to the left
        right_col_x = 3 * self.width // 4 - input_width // 2 + 20  # Move right column more to the right
        
        # Draw basic information section (left column)
        basic_section_y = 100 # Increased from 100
        
        for i, field in enumerate(basic_fields):
            y_pos = basic_section_y + i * input_spacing_v
            
            # Draw label
            label = self.label_font.render(f"{field.capitalize()}:", True, COLORS['text'])
            self.screen.blit(label, (left_col_x, y_pos - 15))
            
            # Draw input field rectangle
            rect = pygame.Rect(left_col_x, y_pos, input_width, input_height)
            input_rects[field] = rect  # Store the rect
            
            # Set background color (highlight if active)
            bg_color = COLORS['input_bg']
            if self.active_field == field:
                bg_color = (220, 220, 255)  # Light purple highlight
            
            self.draw_rounded_rect(self.screen, bg_color, rect, 10)
            self.draw_rounded_rect(self.screen, COLORS['input_border'], rect, 10, 2)
            
            # Draw text inside input field
            text_to_render = self.new_student_data.get(field, "")
            if field == 'password':
                text_to_render = '*' * len(text_to_render)
                
            text_surf = self.text_font.render(text_to_render, True, COLORS['input_text'])
            self.screen.blit(text_surf, (rect.x + 10, rect.y + 10))
        
        # Draw marks section (right column)
        marks_section_y = 100 # Increased from 100
        
        for i, field in enumerate(marks_fields):
            y_pos = marks_section_y + i * input_spacing_v
            
            # Format display label
            display_label = field.replace("marks_", "").capitalize() + " Marks:"
            
            # Draw label
            label = self.label_font.render(display_label, True, COLORS['text'])
            self.screen.blit(label, (right_col_x, y_pos - 15))
            
            # Draw input field rectangle
            rect = pygame.Rect(right_col_x, y_pos, input_width, input_height)
            input_rects[field] = rect  # Store the rect
            
            # Set background color (highlight if active)
            bg_color = COLORS['input_bg']
            if self.active_field == field:
                bg_color = (220, 220, 255)  # Light purple highlight
            
            self.draw_rounded_rect(self.screen, bg_color, rect, 10)
            self.draw_rounded_rect(self.screen, COLORS['input_border'], rect, 10, 2)
            
            # Draw text inside input field
            text_to_render = self.new_student_data.get(field, "")
            text_surf = self.text_font.render(text_to_render, True, COLORS['input_text'])
            self.screen.blit(text_surf, (rect.x + 10, rect.y + 10))
        
        # Draw ECA section (spans both columns at bottom)
        eca_section_y = marks_section_y + len(marks_fields) * input_spacing_v + 60
        eca_title = self.label_font.render("Extra-Curricular Activities", True, COLORS['accent'])
        eca_title_rect = eca_title.get_rect(center=(self.width // 2, eca_section_y - 15))
        self.screen.blit(eca_title, eca_title_rect)
        
        # ECA field spans width of left column
        field = "eca"
        eca_label = self.label_font.render("ECA Activities (comma separated):", True, COLORS['text'])
        self.screen.blit(eca_label, (left_col_x, eca_section_y - 15))
        
        rect = pygame.Rect(left_col_x, eca_section_y, input_width, input_height)
        input_rects[field] = rect  # Store the rect
        
        # Set background color (highlight if active)
        bg_color = COLORS['input_bg']
        if self.active_field == field:
            bg_color = (220, 220, 255)  # Light purple highlight
        
        self.draw_rounded_rect(self.screen, bg_color, rect, 10)
        self.draw_rounded_rect(self.screen, COLORS['input_border'], rect, 10, 2)
        
        # Draw text inside input field
        text_to_render = self.new_student_data.get(field, "")
        text_surf = self.text_font.render(text_to_render, True, COLORS['input_text'])
        self.screen.blit(text_surf, (rect.x + 10, rect.y + 10))
            
        # Calculate button positions
        button_y = eca_section_y + input_height + 60  # Increased vertical spacing
        button_width = 150
        
        # Submit button
        submit_rect = pygame.Rect(
            self.width // 2 - button_width - 20, 
            button_y, 
            button_width, 
            self.button_height
        )
        submit_color = COLORS['success_hover'] if submit_rect.collidepoint(pygame.mouse.get_pos()) else COLORS['success']
        self.draw_rounded_rect(self.screen, submit_color, submit_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], submit_rect, self.button_radius, 2)
        submit_text = self.text_font.render("Add Student", True, WHITE)
        submit_text_rect = submit_text.get_rect(center=submit_rect.center)
        self.screen.blit(submit_text, submit_text_rect)
        
        # Back button
        back_button_rect = pygame.Rect(
            self.width // 2 + 20, 
            button_y, 
            button_width, 
            self.button_height
        )
        back_color = COLORS['button_hover'] if back_button_rect.collidepoint(pygame.mouse.get_pos()) else COLORS['button']
        self.draw_rounded_rect(self.screen, back_color, back_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], back_button_rect, self.button_radius, 2)
        back_text = self.text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)

        # Draw error message if any
        if hasattr(self, 'error_message') and self.error_message:
            error_surf = self.text_font.render(self.error_message, True, COLORS['error'])
            error_rect = error_surf.get_rect(center=(self.width // 2, button_y + self.button_height + 25))
            self.screen.blit(error_surf, error_rect)

        return input_rects, submit_rect, back_button_rect # Return the rects
    
    def delete_student(self, username):
        try:
            # Read all lines from users.txt
            with open('dataset/users.txt', 'r') as file:
                lines = file.readlines()
            
            # Filter out the student to delete
            new_lines = [line for line in lines if not line.startswith(f"{username},")]
            
            # Write back the filtered lines
            with open('dataset/users.txt', 'w') as file:
                file.writelines(new_lines)
            
            # Read all lines from passwords.txt
            with open('dataset/passwords.txt', 'r') as file:
                lines = file.readlines()
            
            # Filter out the student's password
            new_lines = [line for line in lines if not line.startswith(f"{username},")]
            
            # Write back the filtered lines
            with open('dataset/passwords.txt', 'w') as file:
                file.writelines(new_lines)
            
            # Read all lines from grades.txt
            with open('dataset/grades.txt', 'r') as file:
                lines = file.readlines()
            
            # Filter out the student's grades
            new_lines = [line for line in lines if not line.startswith(f"{username},")]
            
            # Write back the filtered lines
            with open('dataset/grades.txt', 'w') as file:
                file.writelines(new_lines)
            
            # Read all lines from eca.txt
            with open('dataset/eca.txt', 'r') as file:
                lines = file.readlines()
            
            # Filter out the student's ECA activities
            new_lines = [line for line in lines if not line.startswith(f"{username},")]
            
            # Write back the filtered lines
            with open('dataset/eca.txt', 'w') as file:
                file.writelines(new_lines)
            
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    def draw_delete_student_form(self):
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.background_color)
        
        # Draw title with shadow
        title = self.title_font.render("Select Student to Delete", True, COLORS['text'])
        shadow = self.title_font.render("Select Student to Delete", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.width // 2 + 2, 82))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Load students
        students = self.load_all_students()
        student_buttons = {} # Initialize dictionary to store button rects
        
        # Layout parameters for student buttons
        button_width = 180
        button_height = 35
        button_spacing_h = 20
        button_spacing_v = 15
        buttons_per_row = 3
        start_x = (self.width - (buttons_per_row * button_width + (buttons_per_row - 1) * button_spacing_h)) // 2
        y_offset = 130 # Start buttons lower
        
        # Draw student buttons in columns
        for i, (username, name, email, phone) in enumerate(students):
            row = i // buttons_per_row
            col = i % buttons_per_row
            
            x_pos = start_x + col * (button_width + button_spacing_h)
            current_y = y_offset + row * (button_height + button_spacing_v)
            
            button_rect = pygame.Rect(x_pos, current_y, button_width, button_height)
            student_buttons[username] = button_rect # Store rect with username key
            is_selected = self.selected_student == username
            
            # Determine button color
            color = COLORS['delete'] if is_selected else COLORS['button']
            if button_rect.collidepoint(pygame.mouse.get_pos()): # Hover effect
                color = COLORS['delete_hover'] if is_selected else COLORS['button_hover']
                
            self.draw_rounded_rect(self.screen, color, button_rect, 5)
            self.draw_rounded_rect(self.screen, COLORS['text'], button_rect, 5, 2)
            
            # Display only the username
            text = self.text_font.render(username, True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
            
        # Calculate position for main buttons based on student list height
        num_rows = (len(students) + buttons_per_row - 1) // buttons_per_row
        last_button_y = y_offset + (num_rows - 1) * (button_height + button_spacing_v) + button_height
        action_button_y = last_button_y + 40
        
        # Ensure buttons don't go off screen, position near bottom if list is short
        action_button_y = max(action_button_y, self.height - 120)
        
        # Draw delete button
        delete_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            action_button_y, # Adjusted Y position
            self.button_width,
            self.button_height
        )
        
        delete_color = COLORS['delete_hover'] if self.selected_student else COLORS['delete'] # Changed inactive color
        if delete_button_rect.collidepoint(pygame.mouse.get_pos()) and self.selected_student:
             delete_color = COLORS['delete_hover']
             
        self.draw_rounded_rect(self.screen, delete_color, delete_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], delete_button_rect, self.button_radius, 2)
        
        delete_text = self.text_font.render("Delete Selected Student", True, WHITE)
        delete_text_rect = delete_text.get_rect(center=delete_button_rect.center)
        self.screen.blit(delete_text, delete_text_rect)
        
        # Draw back button
        back_button_rect = pygame.Rect(
            (self.width - self.button_width) // 2,
            action_button_y + self.button_height + 20, # Position below delete button
            self.button_width,
            self.button_height
        )
        
        back_color = COLORS['button_hover'] if back_button_rect.collidepoint(pygame.mouse.get_pos()) else COLORS['button']
        self.draw_rounded_rect(self.screen, back_color, back_button_rect, self.button_radius)
        self.draw_rounded_rect(self.screen, COLORS['text'], back_button_rect, self.button_radius, 2)
        
        back_text = self.text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        return delete_button_rect, back_button_rect, student_buttons
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        showing_add_student = False
        
        while running:
            mouse_pos = pygame.mouse.get_pos() # Get mouse position once per frame
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if showing_add_student:
                    # Get the rectangles from the drawing function
                    input_rects, submit_rect, back_button_rect = self.draw_add_student_form()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check button clicks first
                        if submit_rect.collidepoint(mouse_pos):
                            if self.add_student():
                                showing_add_student = False
                                self.new_student_data = {
                                    "username": "",
                                    "password": "",
                                    "name": "",
                                    "email": "",
                                    "phone": "",
                                    "marks_math": "",
                                    "marks_science": "",
                                    "marks_english": "",
                                    "marks_history": "",
                                    "marks_computer": "",
                                    "eca": "",
                                }
                        elif back_button_rect.collidepoint(mouse_pos):
                            showing_add_student = False
                            self.new_student_data = {
                                "username": "",
                                "password": "",
                                "name": "",
                                "email": "",
                                "phone": "",
                                "marks_math": "",
                                "marks_science": "",
                                "marks_english": "",
                                "marks_history": "",
                                "marks_computer": "",
                                "eca": "",
                            }
                        else:
                            # Check if any input field was clicked
                            for field, rect in input_rects.items():
                                if rect.collidepoint(mouse_pos):
                                    self.active_field = field
                                    break
                            else:
                                self.active_field = None
                    
                    elif event.type == pygame.KEYDOWN:
                        if self.active_field:
                            if event.key == pygame.K_BACKSPACE:
                                # Remove last character
                                self.new_student_data[self.active_field] = self.new_student_data[self.active_field][:-1]
                            elif event.key == pygame.K_TAB:
                                # Move to next field
                                fields = list(input_rects.keys())
                                current_idx = fields.index(self.active_field) if self.active_field in fields else -1
                                next_idx = (current_idx + 1) % len(fields)
                                self.active_field = fields[next_idx]
                            elif event.key == pygame.K_RETURN:
                                # Treat Enter like clicking submit
                                if self.add_student():
                                    showing_add_student = False
                                    self.new_student_data = {
                                        "username": "",
                                        "password": "",
                                        "name": "",
                                        "email": "",
                                        "phone": "",
                                        "marks_math": "",
                                        "marks_science": "",
                                        "marks_english": "",
                                        "marks_history": "",
                                        "marks_computer": "",
                                        "eca": "",
                                    }
                            else:
                                # For marks fields, only allow digits
                                if self.active_field.startswith("marks_") and not event.unicode.isdigit():
                                    pass # Ignore non-digit input for marks
                                else:
                                    # Add typed character to the active field
                                    self.new_student_data[self.active_field] += event.unicode
                                
                elif self.showing_delete_student:
                    # Get all button rects from the drawing function
                    delete_button_rect, back_button_rect, student_buttons = self.draw_delete_student_form()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if delete_button_rect.collidepoint(mouse_pos) and self.selected_student:
                            if self.delete_student(self.selected_student):
                                self.showing_delete_student = False
                                self.selected_student = None
                        
                        elif back_button_rect.collidepoint(mouse_pos):
                            self.showing_delete_student = False
                            self.selected_student = None
                        else:
                            # Check clicks on student buttons
                            for username, rect in student_buttons.items():
                                if rect.collidepoint(mouse_pos):
                                    self.selected_student = username
                                    break
                else:
                    # Main menu event handling
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.is_admin:
                            if self.add_student_button_rect.collidepoint(mouse_pos):
                                showing_add_student = True
                                self.active_field = None # Reset active field when entering form
                                self.error_message = "" # Clear any previous error message
                            elif self.delete_student_button_rect.collidepoint(mouse_pos):
                                self.showing_delete_student = True
                                self.selected_student = None # Reset selected student
                            elif self.view_students_button_rect.collidepoint(mouse_pos):
                                DataDisplayWindow(self.load_all_students(), "students", self.is_admin, self)
                            elif self.visualize_marks_button_rect.collidepoint(mouse_pos):
                                DataDisplayWindow(self.visualize_marks(), "visualization", self.is_admin, self)
                        
                        if self.marks_button_rect.collidepoint(mouse_pos):
                            DataDisplayWindow(self.load_marks(), "marks", self.is_admin, self)
                        elif self.eca_button_rect.collidepoint(mouse_pos):
                            DataDisplayWindow(self.load_eca(), "eca", self.is_admin, self)
                        elif self.logout_button_rect.collidepoint(mouse_pos):
                            running = False
                            pygame.quit()
                            from simple_ui import MenuUI
                            MenuUI()
                        elif self.back_button_rect.collidepoint(mouse_pos):
                            running = False
                            pygame.quit()
                            from simple_ui import MenuUI
                            MenuUI()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if showing_add_student:
                            showing_add_student = False
                            self.new_student_data = {
                                "username": "",
                                "password": "",
                                "name": "",
                                "email": "",
                                "phone": "",
                                "marks_math": "",
                                "marks_science": "",
                                "marks_english": "",
                                "marks_history": "",
                                "marks_computer": "",
                                "eca": "",
                            }
                        elif self.showing_delete_student:
                            self.showing_delete_student = False
                            self.selected_student = None
                        else:
                            running = False
                            pygame.quit()
                            from simple_ui import MenuUI
                            MenuUI()
            
            # Draw background
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            else:
                self.screen.fill(self.background_color)
            
            # Draw logo if available
            if self.logo:
                self.screen.blit(self.logo, (self.width - 120, 20))
            
            if showing_add_student:
                self.draw_add_student_form()
            elif self.showing_delete_student:
                self.draw_delete_student_form()
            else: # This is the main menu view
                # Draw title with shadow - ADDED HERE
                shadow = self.title_font.render(self.title_text, True, (0, 0, 0))
                shadow_rect = shadow.get_rect(center=(self.width // 2 + 2, 82))
                title_rect = self.title_surface.get_rect(center=(self.width // 2, 80))
                self.screen.blit(shadow, shadow_rect)
                self.screen.blit(self.title_surface, title_rect)
                
                mouse_pos = pygame.mouse.get_pos()
                
                if self.is_admin:
                    # Add Student button
                    add_color = COLORS['button_hover'] if self.add_student_button_rect.collidepoint(mouse_pos) else COLORS['button']
                    self.draw_rounded_rect(self.screen, add_color, self.add_student_button_rect, self.button_radius)
                    self.draw_rounded_rect(self.screen, COLORS['text'], self.add_student_button_rect, self.button_radius, 2)
                    
                    add_text = self.text_font.render("Add Student", True, WHITE)
                    add_text_rect = add_text.get_rect(center=self.add_student_button_rect.center)
                    self.screen.blit(add_text, add_text_rect)
                    
                    # Delete Student button
                    delete_color = COLORS['delete_hover'] if self.delete_student_button_rect.collidepoint(mouse_pos) else COLORS['delete']
                    self.draw_rounded_rect(self.screen, delete_color, self.delete_student_button_rect, self.button_radius)
                    self.draw_rounded_rect(self.screen, COLORS['text'], self.delete_student_button_rect, self.button_radius, 2)
                    
                    delete_text = self.text_font.render("Delete Student", True, WHITE)
                    delete_text_rect = delete_text.get_rect(center=self.delete_student_button_rect.center)
                    self.screen.blit(delete_text, delete_text_rect)
                    
                    # View Students button
                    view_color = COLORS['button_hover'] if self.view_students_button_rect.collidepoint(mouse_pos) else COLORS['button']
                    self.draw_rounded_rect(self.screen, view_color, self.view_students_button_rect, self.button_radius)
                    self.draw_rounded_rect(self.screen, COLORS['text'], self.view_students_button_rect, self.button_radius, 2)
                    
                    view_text = self.text_font.render("View All Students", True, WHITE)
                    view_text_rect = view_text.get_rect(center=self.view_students_button_rect.center)
                    self.screen.blit(view_text, view_text_rect)
                    
                    # Visualize Marks button
                    viz_color = COLORS['button_hover'] if self.visualize_marks_button_rect.collidepoint(mouse_pos) else COLORS['button']
                    self.draw_rounded_rect(self.screen, viz_color, self.visualize_marks_button_rect, self.button_radius)
                    self.draw_rounded_rect(self.screen, COLORS['text'], self.visualize_marks_button_rect, self.button_radius, 2)
                    
                    viz_text = self.text_font.render("Visualize Marks", True, WHITE)
                    viz_text_rect = viz_text.get_rect(center=self.visualize_marks_button_rect.center)
                    self.screen.blit(viz_text, viz_text_rect)
                
                # View Marks button
                marks_color = COLORS['button_hover'] if self.marks_button_rect.collidepoint(mouse_pos) else COLORS['button']
                self.draw_rounded_rect(self.screen, marks_color, self.marks_button_rect, self.button_radius)
                self.draw_rounded_rect(self.screen, COLORS['text'], self.marks_button_rect, self.button_radius, 2)
                
                marks_text = self.text_font.render("View Marks", True, WHITE)
                marks_text_rect = marks_text.get_rect(center=self.marks_button_rect.center)
                self.screen.blit(marks_text, marks_text_rect)
                
                # View ECA button
                eca_color = COLORS['button_hover'] if self.eca_button_rect.collidepoint(mouse_pos) else COLORS['button']
                self.draw_rounded_rect(self.screen, eca_color, self.eca_button_rect, self.button_radius)
                self.draw_rounded_rect(self.screen, COLORS['text'], self.eca_button_rect, self.button_radius, 2)
                
                eca_text = self.text_font.render("View ECA Activities", True, WHITE)
                eca_text_rect = eca_text.get_rect(center=self.eca_button_rect.center)
                self.screen.blit(eca_text, eca_text_rect)
                
                # Logout button
                logout_color = COLORS['delete_hover'] if self.logout_button_rect.collidepoint(mouse_pos) else COLORS['delete']
                self.draw_rounded_rect(self.screen, logout_color, self.logout_button_rect, self.button_radius)
                self.draw_rounded_rect(self.screen, COLORS['text'], self.logout_button_rect, self.button_radius, 2)
                
                logout_text = self.text_font.render("Logout", True, WHITE)
                logout_text_rect = logout_text.get_rect(center=self.logout_button_rect.center)
                self.screen.blit(logout_text, logout_text_rect)
                
                # Back button
                back_color = COLORS['button_hover'] if self.back_button_rect.collidepoint(mouse_pos) else COLORS['button']
                self.draw_rounded_rect(self.screen, back_color, self.back_button_rect, self.button_radius)
                self.draw_rounded_rect(self.screen, COLORS['text'], self.back_button_rect, self.button_radius, 2)
                
                back_text = self.text_font.render("Back to Menu", True, WHITE)
                back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
                self.screen.blit(back_text, back_text_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = UserManagement("test_user") 