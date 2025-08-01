# player.py
import pygame
from character_sprite import CharacterSprite

class Player:
    def __init__(self, name, sprite_path, sprite_width, sprite_height, num_frames, sprite_scale, max_health, attack, speed):
        self.name = name
        self.sprite = CharacterSprite(sprite_path, sprite_width, sprite_height, num_frames, scale=sprite_scale)
        self.max_health = max_health
        self.current_health = max_health 
        self.attack = attack
        self.speed = speed
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.sprite.set_position(x, y) 

    def get_position(self):
        return self.x, self.y

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
        # print(f"{self.name} recibió {amount} de daño. Salud restante: {self.current_health}") # Puedes descomentar esto para depuración

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        # print(f"{self.name} se curó {amount}. Salud actual: {self.current_health}") # Puedes descomentar esto para depuración

    def update(self):
        self.sprite.update()

    def draw(self, screen):
        self.sprite.draw(screen)