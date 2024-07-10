import pygame

class Screen:
    def __init__(self):
        self.display = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption('Pokemon Clone')
        self.clock = pygame.time.Clock()
        self.framerate = 144
        self.deltatime: float = 0.0
        self.imagescreen = pygame.display.get_surface()
        
    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.imagescreen = self.display.copy()
        self.display.fill((0, 0, 0))
        self.deltatime = self.clock.get_time()
        
        
    def get_delta_time(self):
        return self.deltatime    
        
    
    def get_size(self):
        return self.display.get_size()
    
    def get_display(self):
        return self.display
    
    def image_screen(self):
        return self.imagescreen.copy()