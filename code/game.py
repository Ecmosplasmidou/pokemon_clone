import pygame
from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()   
        self.player = Player(self.keylistener, self.screen, 0, 0)
        self.map.add_player(self.player)
                
        
    def run(self):
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_keys(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_keys(event.key)