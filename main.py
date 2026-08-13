import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window Setup
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sterile")
clock = pygame.time.Clock()
fullscreen = False

# Colors
COLOR_BG = (240, 245, 250)      # Light blue-gray background
COLOR_WATER = (64, 165, 220)    # Clean water blue
COLOR_DIRT = (139, 69, 19)      # Muddy brown
COLOR_TEXT = (40, 40, 40)

# Filter Layer Colors
COLOR_SAND = (235, 210, 160)     # Light sand beige
COLOR_CHARCOAL = (50, 50, 50)    # Dark charcoal gray
COLOR_SOCK = (220, 220, 220)     # Off-white fabric

# Simulation Settings
PARTICLE_COUNT = 150
GRAVITY = 1.2
MIN_PARTICLES = 10
MAX_PARTICLES = 500

# Define Filter Structure Layout
# Top to bottom: Sand (10cm equivalent) -> Charcoal (5cm equivalent) -> Sock (Base)
FILTER_LEFT = 350
FILTER_RIGHT = 700
FILTER_WIDTH = FILTER_RIGHT - FILTER_LEFT

SAND_TOP = 200
SAND_BOTTOM = 350 # 150px thick (representing 10cm)

CHARCOAL_TOP = 350
CHARCOAL_BOTTOM = 425 # 75px thick (representing 5cm)

SOCK_TOP = 425
SOCK_BOTTOM = 450 # 25px thick base sieve

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, value=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.value = value
        self.hovered = False

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ScrollableInfo:
    def __init__(self, x, y, width, height, font, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.scroll_offset = 0
        self.line_height = 20
        self.text_lines = [
            "FILTER LAYERS:",
            "",
            "1. Fine Sand Layer (10 cm)",
            "   - Traps smaller dirt particles",
            "   - Slows down water flow",
            "   - Removes 1% of particles per frame",
            "",
            "2. Activated Charcoal (5 cm)",
            "   - Removes odors and chemicals",
            "   - Adsorbs impurities via absorption",
            "   - Removes 5% of particles per frame",
            "",
            "3. Cotton Sock Base",
            "   - Final physical sieve",
            "   - Catches micro-sediment",
            "   - 100% particle removal",
            "",
            "CONTROLS:",
            "- Use ±1, ±10, ±50 buttons to adjust",
            "- Click 'Drop Water' to start simulation",
            "- Press F11 for fullscreen mode"
        ]

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (245, 245, 245), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        
        # Draw text
        y_offset = self.rect.y - self.scroll_offset
        for line in self.text_lines:
            if y_offset + self.line_height > self.rect.y and y_offset < self.rect.y + self.rect.height:
                text_surf = self.font.render(line, True, self.text_color)
                surface.blit(text_surf, (self.rect.x + 10, y_offset))
            y_offset += self.line_height

    def scroll(self, amount):
        max_scroll = max(0, len(self.text_lines) * self.line_height - self.rect.height)
        self.scroll_offset = max(0, min(self.scroll_offset + amount, max_scroll))

class WaterParticle:
    def __init__(self):
        self.reset()
        # Randomise initial heights so they don't all drop at once
        self.y = random.randint(-200, 50)

    def reset(self):
        self.x = random.randint(FILTER_LEFT + 20, FILTER_RIGHT - 20)
        self.y = random.randint(-100, -10)
        self.is_dirty = True
        self.speed_modifier = 1.0

    def update(self):
        # Apply variable speed depending on the filter layer density
        current_speed = GRAVITY * self.speed_modifier
        self.y += current_speed

        # LAYER 1: Sand Layer (10 cm)
        # Traps smaller dirt particles, slows down flow
        if SAND_TOP <= self.y < SAND_BOTTOM:
            self.speed_modifier = 0.4
            # Probability to clean large dirt particles early
            if self.is_dirty and random.random() < 0.01:
                self.is_dirty = False

        # LAYER 2: Activated Charcoal Layer (5 cm)
        # Adsorbs remaining microscopic impurities and chemical stains
        elif CHARCOAL_TOP <= self.y < CHARCOAL_BOTTOM:
            self.speed_modifier = 0.3
            if self.is_dirty and random.random() < 0.05:
                self.is_dirty = False

        # LAYER 3: Cotton Sock Base
        # Final physical sieve holding media, catches micro-sediment
        elif SOCK_TOP <= self.y < SOCK_BOTTOM:
            self.speed_modifier = 0.2
            self.is_dirty = False # Fully cleared by the final fabric sieve

        # Free fall outside filter zones
        else:
            self.speed_modifier = 1.5

        # Reset particle once it flows off the screen
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surface):
        color = COLOR_DIRT if self.is_dirty else COLOR_WATER
        radius = 5 if self.is_dirty else 4
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)

# Create particle list
particles = []
current_particle_count = PARTICLE_COUNT

# Create buttons (value is the amount to add/subtract)
btn_minus_50 = Button(20, 700, 70, 40, "-50", (200, 100, 100), (255, 255, 255), -50)
btn_minus_10 = Button(100, 700, 70, 40, "-10", (200, 100, 100), (255, 255, 255), -10)
btn_minus_1 = Button(180, 700, 70, 40, "-1", (200, 100, 100), (255, 255, 255), -1)
btn_plus_1 = Button(260, 700, 70, 40, "+1", (100, 200, 100), (255, 255, 255), 1)
btn_plus_10 = Button(340, 700, 70, 40, "+10", (100, 200, 100), (255, 255, 255), 10)
btn_plus_50 = Button(420, 700, 70, 40, "+50", (100, 200, 100), (255, 255, 255), 50)
btn_drop = Button(520, 700, 150, 40, "Drop Water", (64, 165, 220), (255, 255, 255))

# Font setup
font_title = pygame.font.SysFont("Arial", 24, bold=True)
font_label = pygame.font.SysFont("Arial", 16, bold=True)
font_desc = pygame.font.SysFont("Arial", 14)

# Create scrollable info panel
info_panel = ScrollableInfo(750, 200, 420, 550, font_desc, COLOR_TEXT)

# Main Simulation Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if btn_minus_50.is_clicked(mouse_pos):
                current_particle_count = max(MIN_PARTICLES, current_particle_count - 50)
            elif btn_minus_10.is_clicked(mouse_pos):
                current_particle_count = max(MIN_PARTICLES, current_particle_count - 10)
            elif btn_minus_1.is_clicked(mouse_pos):
                current_particle_count = max(MIN_PARTICLES, current_particle_count - 1)
            elif btn_plus_1.is_clicked(mouse_pos):
                current_particle_count = min(MAX_PARTICLES, current_particle_count + 1)
            elif btn_plus_10.is_clicked(mouse_pos):
                current_particle_count = min(MAX_PARTICLES, current_particle_count + 10)
            elif btn_plus_50.is_clicked(mouse_pos):
                current_particle_count = min(MAX_PARTICLES, current_particle_count + 50)
            elif btn_drop.is_clicked(mouse_pos):
                # Add all particles at once
                particles = [WaterParticle() for _ in range(current_particle_count)]
        elif event.type == pygame.MOUSEWHEEL:
            info_panel.scroll(event.y * 10)

    # Clear screen
    screen.fill(COLOR_BG)

    # -------------------------------------------------------------
    # DRAW STATIC FILTER GRAPHICS
    # -------------------------------------------------------------
    
    # 1. Sand Layer Block
    pygame.draw.rect(screen, COLOR_SAND, (FILTER_LEFT, SAND_TOP, FILTER_WIDTH, SAND_BOTTOM - SAND_TOP))
    # Sand texture detail
    for _ in range(10):
        rx = random.randint(FILTER_LEFT, FILTER_RIGHT)
        ry = random.randint(SAND_TOP, SAND_BOTTOM)
        pygame.draw.circle(screen, (215, 190, 140), (rx, ry), 1)

    # 2. Activated Charcoal Layer Block
    pygame.draw.rect(screen, COLOR_CHARCOAL, (FILTER_LEFT, CHARCOAL_TOP, FILTER_WIDTH, CHARCOAL_BOTTOM - CHARCOAL_TOP))
    # Charcoal texture detail
    for _ in range(8):
        rx = random.randint(FILTER_LEFT, FILTER_RIGHT)
        ry = random.randint(CHARCOAL_TOP, CHARCOAL_BOTTOM)
        pygame.draw.rect(screen, (30, 30, 30), (rx, ry, 4, 4))

    # 3. Cotton Sock Layer Block
    pygame.draw.rect(screen, COLOR_SOCK, (FILTER_LEFT, SOCK_TOP, FILTER_WIDTH, SOCK_BOTTOM - SOCK_TOP))

    # Outer Container Outlines
    pygame.draw.line(screen, (100, 100, 100), (FILTER_LEFT, 100), (FILTER_LEFT, SOCK_BOTTOM), 3)
    pygame.draw.line(screen, (100, 100, 100), (FILTER_RIGHT, 100), (FILTER_RIGHT, SOCK_BOTTOM), 3)

    # -------------------------------------------------------------
    # DRAW LABELS AND INSTRUCTIONS
    # -------------------------------------------------------------
    
    # Title
    title_text = font_title.render("Sterile", True, COLOR_TEXT)
    screen.blit(title_text, (20, 20))

    # Sand Text
    screen.blit(font_label.render("1. Fine Sand Layer (10 cm)", True, COLOR_TEXT), (50, SAND_TOP + 10))
    screen.blit(font_desc.render("Traps smaller dirt particles", True, COLOR_TEXT), (50, SAND_TOP + 30))

    # Charcoal Text
    screen.blit(font_label.render("2. Activated Charcoal (5 cm)", True, COLOR_TEXT), (50, CHARCOAL_TOP + 10))
    screen.blit(font_desc.render("Removes odors and chemicals", True, COLOR_TEXT), (50, CHARCOAL_TOP + 30))

    # Sock Text
    screen.blit(font_label.render("3. Cotton Sock Base", True, COLOR_TEXT), (50, SOCK_TOP + 2))
    screen.blit(font_desc.render("Final physical sieve", True, COLOR_TEXT), (50, SOCK_TOP + 20))

    # Particle Count Display
    particle_text = font_label.render(f"Particles to Drop: {current_particle_count}", True, COLOR_TEXT)
    screen.blit(particle_text, (50, 660))

    # Draw Info Panel
    info_panel.draw(screen)

    # Draw Buttons
    btn_minus_50.draw(screen, font_label)
    btn_minus_10.draw(screen, font_label)
    btn_minus_1.draw(screen, font_label)
    btn_plus_1.draw(screen, font_label)
    btn_plus_10.draw(screen, font_label)
    btn_plus_50.draw(screen, font_label)
    btn_drop.draw(screen, font_label)

    # -------------------------------------------------------------
    # UPDATE AND DRAW PARTICLES
    # -------------------------------------------------------------
    for particle in particles:
        particle.update()
        particle.draw(screen)

    # Render Frame
    pygame.display.flip()
    clock.tick(60)
