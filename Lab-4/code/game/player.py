import pygame

class Player:
    def __init__(self, x, y, width=24, height=32, speed=4, jump_strength=-12):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.jump_strength = jump_strength
        self.on_ground = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def jump(self):
        """Attempts to jump if the player is currently grounded. Returns True if jump started."""
        if self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
            return True
        return False

    def reset_position(self, x, y):
        """Resets positional kinematics."""
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = False
