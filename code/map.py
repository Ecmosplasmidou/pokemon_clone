import pygame
import pytmx
import pyscroll

from screen import Screen
from player import Player
from switch import Switch

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map = None
        self.group = None
        
        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collision: list[pygame.Rect] | None = None
        
        self.current_map: Switch = Switch("switch", "map_0", pygame.Rect(0, 0, 0, 0), 0)
        
        self.switch_map(self.current_map)
        
        
        
    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.util_pygame.load_pygame(f"assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)
        
        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 2.5
            
            
        self.switchs = []
        self.collision = []
        
        
                
        for obj in self.tmx_data.objects:
            if obj.name:  # Vérifiez si obj.name n'est pas None
                type = obj.name.split(" ")[0]
                if type == "collision":
                    self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                elif type == "switch":
                    self.switchs.append(Switch(type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height), int(obj.name.split(" ")[-1])))
                
        
        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collision(self.collision)
            self.group.add(self.player)
            if switch.name.split("_")[0] == "house": 
                self.player.switch_bike(True)
            
        self.current_map = switch
        
    def add_player (self, player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collision(self.collision)
        
        
    def update(self) -> None:
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None
        self.group.update()
        self.group.draw(self.screen.get_display())
        self.group.center(self.player.rect.center)
        
        
    def pose_player(self, switch: Switch) -> None:
        position = self.tmx_data.get_object_by_name("spawn" + " " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)
        