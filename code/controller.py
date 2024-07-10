import pygame

class Controller:
    def __init__(self):
        self.keys = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'bike': pygame.K_SPACE,
            'action': pygame.K_e,
            'fullscreen': pygame.K_f,
            "escape": pygame.K_ESCAPE,
        }
        
    
    def get_key(self, key: str) -> int:
        return self.keys[key]
    
    def add_key(self, key: str, value: int):
        self.keys[key] = value