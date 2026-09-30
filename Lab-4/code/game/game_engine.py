import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard
from .sounds import SoundManager

# Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (150, 100, 60)
PLATFORM_TOP = (180, 130, 90)
RED = (220, 60, 60)
GREEN = (40, 200, 70)
YELLOW = (255, 215, 0)
CYAN = (0, 220, 240)
DARK_OVERLAY = (20, 24, 34, 210)
PANEL_BG = (35, 42, 58)
PANEL_BORDER = (90, 105, 140)

def safe_font(size, bold=False):
    """Safely retrieves a font, falling back to pygame default if SysFont is restricted."""
    try:
        f = pygame.font.SysFont("Arial", size, bold=bold)
        if f:
            return f
    except Exception:
        pass
    return pygame.font.Font(None, size)

class GameEngine:
    DIFFICULTIES = {
        "easy": {
            "name": "Easy",
            "gravity": 0.45,
            "jump_strength": -13.0,
            "speed": 4.5,
            "terminal_velocity": 12.0,
            "desc": "Low Gravity, High Jump"
        },
        "medium": {
            "name": "Medium",
            "gravity": 0.60,
            "jump_strength": -12.0,
            "speed": 4.0,
            "terminal_velocity": 14.0,
            "desc": "Balanced Classic Physics"
        },
        "hard": {
            "name": "Hard",
            "gravity": 0.85,
            "jump_strength": -11.5,
            "speed": 3.8,
            "terminal_velocity": 16.0,
            "desc": "Heavy Gravity, Strict Timing"
        }
    }

    def __init__(self, width, height, initial_difficulty="medium"):
        self.width = width
        self.height = height
        self.start_x, self.start_y = 40, height - 120
        self.goal_x = 740

        # Sound Manager (Task 4)
        self.sounds = SoundManager()

        # State management (Task 2 & 3)
        self.state = "PLAYING"
        self.game_over = False
        self.should_quit = False
        self.score = 0
        self.high_score = 0
        self.difficulty = initial_difficulty

        # Fonts
        self.font = safe_font(26)
        self.font_large = safe_font(44, bold=True)
        self.font_medium = safe_font(24, bold=True)
        self.font_small = safe_font(20)

        # Setup level geometry & player
        self.player = Player(self.start_x, self.start_y)
        self._init_level()
        self.apply_difficulty(self.difficulty)

    def _init_level(self):
        ground_y = self.height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(240, ground_y - 14, 100)]

    def apply_difficulty(self, diff_key):
        """Configures physics parameters for chosen difficulty setting (Task 3)."""
        diff = self.DIFFICULTIES.get(diff_key, self.DIFFICULTIES["medium"])
        self.difficulty = diff_key
        self.gravity = diff["gravity"]
        self.terminal_velocity = diff["terminal_velocity"]
        self.player.speed = diff["speed"]
        self.player.jump_strength = diff["jump_strength"]

    def reset(self, difficulty=None):
        """Resets the game state for replaying (Task 3)."""
        if difficulty:
            self.apply_difficulty(difficulty)
        self.player.reset_position(self.start_x, self.start_y)
        self.score = 0
        self.state = "PLAYING"
        self.game_over = False

    def trigger_game_over(self):
        """Transitions into the Game Over state and plays sound feedback (Task 2 & 4)."""
        if self.state != "GAME_OVER":
            self.state = "GAME_OVER"
            self.game_over = True
            self.sounds.play_death()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "PLAYING":
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.player.jump():
                        self.sounds.play_jump() # Task 4
            elif self.state == "GAME_OVER":
                # Task 3: Difficulty selection & replay
                if event.key in (pygame.K_1, pygame.K_e):
                    self.reset(difficulty="easy")
                elif event.key in (pygame.K_2, pygame.K_m):
                    self.reset(difficulty="medium")
                elif event.key in (pygame.K_3, pygame.K_h):
                    self.reset(difficulty="hard")
                elif event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                    self.reset(difficulty=self.difficulty)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.should_quit = True

    def handle_input(self):
        if self.state != "PLAYING":
            return
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.state != "PLAYING":
            return

        # Continuous Collision Detection & Physics (Task 1)
        # 1. Apply gravity with terminal velocity capping
        self.player.vy = min(self.terminal_velocity, self.player.vy + self.gravity)

        # 2. Horizontal movement with screen boundaries
        self.player.x = max(0, min(self.width - self.player.width, self.player.x + self.player.vx))

        # 3. Swept vertical collision detection
        old_y = self.player.y
        old_bottom = old_y + self.player.height
        new_y = old_y + self.player.vy
        new_bottom = new_y + self.player.height

        landed_platform = None
        if self.player.vy >= 0:
            # Sweeping downward: check if player crosses top of any platform
            for platform in self.platforms:
                p_rect = platform.rect()
                # Check horizontal alignment
                if (self.player.x + self.player.width > p_rect.left + 2) and (self.player.x < p_rect.right - 2):
                    # Swept check: was above platform top before and reaches/passes it now
                    if old_bottom <= p_rect.top + 4 and new_bottom >= p_rect.top:
                        if landed_platform is None or p_rect.top < landed_platform.rect().top:
                            landed_platform = platform

        if landed_platform is not None:
            # Snap player directly onto platform surface
            self.player.y = landed_platform.rect().top - self.player.height
            self.player.vy = 0
            self.player.on_ground = True
        else:
            self.player.y = new_y
            self.player.on_ground = False

            # Check head collision if moving upward
            if self.player.vy < 0:
                for platform in self.platforms:
                    p_rect = platform.rect()
                    if (self.player.x + self.player.width > p_rect.left + 2) and (self.player.x < p_rect.right - 2):
                        if old_y >= p_rect.bottom - 4 and new_y <= p_rect.bottom:
                            self.player.y = p_rect.bottom
                            self.player.vy = 0
                            break

        # 4. Check hazard collisions (Task 2)
        p_box = self.player.rect()
        for hazard in self.hazards:
            if p_box.colliderect(hazard.rect()):
                self.trigger_game_over()
                return

        # 5. Check falling off bottom of screen (Task 2)
        if self.player.y > self.height:
            self.trigger_game_over()
            return

        # 6. Check reaching goal line (Task 4)
        if self.player.x >= self.goal_x:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.sounds.play_goal()
            self.player.reset_position(self.start_x, self.start_y)

    def render(self, screen):
        # Draw platforms
        for platform in self.platforms:
            r = platform.rect()
            pygame.draw.rect(screen, BROWN, r)
            pygame.draw.rect(screen, PLATFORM_TOP, (r.x, r.y, r.width, 3))

        # Draw hazards
        for hazard in self.hazards:
            hr = hazard.rect()
            pygame.draw.rect(screen, RED, hr)
            # Decorative spikes / hazard highlights
            for sx in range(hr.x + 5, hr.right, 15):
                pygame.draw.line(screen, YELLOW, (sx, hr.bottom), (sx + 5, hr.top), 2)

        # Draw goal
        goal_rect = pygame.Rect(self.goal_x, 0, 8, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        # Draw player
        pygame.draw.rect(screen, WHITE, self.player.rect(), border_radius=3)
        # Player eye / visor for visual charm
        eye_rect = pygame.Rect(int(self.player.x + 14), int(self.player.y + 6), 6, 6)
        pygame.draw.rect(screen, (30, 40, 60), eye_rect)

        # HUD: Score and Active Difficulty
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (16, 12))

        diff_info = self.DIFFICULTIES.get(self.difficulty, {})
        diff_text = self.font_small.render(f"Difficulty: {diff_info.get('name', 'Medium')}", True, CYAN)
        screen.blit(diff_text, (16, 42))

        high_text = self.font_small.render(f"Best: {self.high_score}", True, YELLOW)
        screen.blit(high_text, (16, 64))

        # Task 2 & 3: Game Over Screen Overlay
        if self.state == "GAME_OVER":
            self._render_game_over_screen(screen)

    def _render_game_over_screen(self, screen):
        """Renders the game over screen with score, difficulty selector, and restart prompts."""
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(DARK_OVERLAY)
        screen.blit(overlay, (0, 0))

        # Central panel
        panel_w, panel_h = 520, 310
        panel_x = (self.width - panel_w) // 2
        panel_y = (self.height - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, panel_rect, width=3, border_radius=12)

        # Header: GAME OVER
        title_surf = self.font_large.render("GAME OVER", True, RED)
        title_rect = title_surf.get_rect(center=(self.width // 2, panel_y + 40))
        screen.blit(title_surf, title_rect)

        # Final Score
        score_surf = self.font_medium.render(f"Final Score: {self.score}   |   Best: {self.high_score}", True, YELLOW)
        score_rect = score_surf.get_rect(center=(self.width // 2, panel_y + 85))
        screen.blit(score_surf, score_rect)

        # Divider line
        pygame.draw.line(screen, PANEL_BORDER, (panel_x + 30, panel_y + 115), (panel_x + panel_w - 30, panel_y + 115), 1)

        # Difficulty Selection instructions (Task 3)
        diff_label = self.font_small.render("SELECT DIFFICULTY TO REPLAY:", True, WHITE)
        diff_label_rect = diff_label.get_rect(center=(self.width // 2, panel_y + 138))
        screen.blit(diff_label, diff_label_rect)

        # Options for difficulties
        options = [
            ("[1] Easy", "easy", panel_x + 80),
            ("[2] Medium", "medium", panel_x + 230),
            ("[3] Hard", "hard", panel_x + 380),
        ]
        for label, key, opt_x in options:
            is_sel = (self.difficulty == key)
            col = CYAN if is_sel else (180, 190, 200)
            prefix = "> " if is_sel else ""
            opt_surf = self.font_small.render(f"{prefix}{label}", True, col)
            opt_rect = opt_surf.get_rect(center=(opt_x, panel_y + 172))
            screen.blit(opt_surf, opt_rect)

        # Action hints
        prompt_replay = self.font_small.render("Press [R] or [SPACE] to Play Again", True, GREEN)
        pr_rect = prompt_replay.get_rect(center=(self.width // 2, panel_y + 225))
        screen.blit(prompt_replay, pr_rect)

        prompt_quit = self.font_small.render("Press [Q] or [ESC] to Exit", True, (160, 160, 160))
        pq_rect = prompt_quit.get_rect(center=(self.width // 2, panel_y + 258))
        screen.blit(prompt_quit, pq_rect)
