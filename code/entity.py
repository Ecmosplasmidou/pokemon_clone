import pygame
from tool import Tool
from screen import Screen

class Entity(pygame.sprite.Sprite):
    def __init__(self, screen : Screen, x: int, y: int):
        super().__init__()
        self.screen: Screen = screen
        self.spritesheet = pygame.image.load("assets/sprite/hero_01_red_m_walk.png")
        self.image = Tool.split_image(self.spritesheet, 0, 0, 24, 32)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        self.rect : pygame.Rect = self.image.get_rect()
        self.all_images: dict[str, list[pygame.Surface]] = self.get_all_images(self.spritesheet)
        self.reset_animation: bool = False    
        self.image_part = 0
        self.index_image = 0
        
        self.hitbox: pygame.Rect =  pygame.Rect(0, 0, 16, 16)  
        self.step: int = 0
        self.animation_walk: bool = False
        self.direction = "down"
        
        self.animation_step_time: float = 0.0
        self.action_animation = 16
        
        self.speed: int = 1
    
    def update(self):
        self.animation_sprite()
        self.move()
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.image = self.all_images[self.direction][self.index_image]


    def move_left(self):
        self.animation_walk = True
        self.direction = "left"
        
    def move_right(self):
        self.animation_walk = True
        self.direction = "right"
        
    def move_up(self):
        self.animation_walk = True
        self.direction = "up"
        
    def move_down(self):
        self.animation_walk = True
        self.direction = "down"
        
    
    def animation_sprite(self):
        if int(self.step//8) + self.image_part >= 4:
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step//8) + self.image_part
        
        
        
    def move(self):
        if self.animation_walk:
            self.animation_step_time += self.screen.get_delta_time()
            if self.step < 16 and self.animation_step_time > self.action_animation:
                self.step += self.speed
                if self.direction == "left":
                    self.position.x -= self.speed
                elif self.direction == "right":
                    self.position.x += self.speed
                elif self.direction == "up":
                    self.position.y -= self.speed
                elif self.direction == "down":
                    self.position.y += self.speed
                self.animation_step_time = 0
            elif self.step >= 16:
                self.step = 0
                self.animation_walk = False
                if self .reset_animation:
                    self.reset_animation = False
                else:
                    if self.image_part == 0:
                        self.image_part = 2
                    else:
                        self.image_part = 0
        
        
    def align_hitbox(self):
        self.position.x += 16
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0:
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0:
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)
        
        
    def get_all_images(self, spritesheet) -> dict[str, list[pygame.Surface]]:
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        
        width: int = spritesheet.get_width()//4
        height: int = spritesheet.get_height()//4
        
        for x in range(4):
            for i, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(spritesheet, x*width, i*height, width, height))
        return all_images