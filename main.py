import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from random import randint
import pygame


class PlanetLandscape:
    def __init__(self):
        noise = PerlinNoise(octaves=24)
        noise2 = PerlinNoise(octaves=32)
        noise3 = PerlinNoise(octaves=2)
        noise4 = PerlinNoise(octaves=8)
        landscape = []
        terrarian_scale = 300
        for x in range(terrarian_scale):
            row = []
            for y in range(terrarian_scale):
                noise_val = noise([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.5 * noise2([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.25 * noise3([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.125 * noise4([x / terrarian_scale, y / terrarian_scale])
                row.append(noise_val)
            landscape.append(row)
        self.landscape = np.array(landscape)
        print(landscape)


    def render(self, screen):
        for x in range(300):
            for y in range(300):
                if self.landscape[x][y] >= 0.2:
                    if self.landscape[x][y] <= 0.25:
                        pygame.draw.rect(screen, (244, 164, 96), (x * 16, y * 16, 16, 16))
                    if self.landscape[x][y] <= 0.33:
                        pygame.draw.rect(screen, (63, 94, 179), (x * 16, y * 16, 16, 16))
                    else:
                        pygame.draw.rect(screen, (81, 114, 175), (x * 16, y * 16, 16, 16))
                else:
                    """if self.landscape[x][y] <= 0.7:
                        pygame.draw.rect(screen, (255, 250, 250), (x * 16, y * 16, 16, 16))
                    else:"""
                    pygame.draw.rect(screen, (0, 158, 0), (x * 16, y * 16, 16, 16))
        return screen



class Player:
    def __init__(self):
        self.cords = [0, 0]

    def renderPlayer(self, screen, cords):
        pygame.draw.rect(screen, 'red', (cords[0], cords[1], 10, 10))
        return screen


if __name__ == '__main__':
    planet = PlanetLandscape()
    running = True
    screen = pygame.display.set_mode([1500, 1000])
    player = Player()
    clock = pygame.time.Clock()
    cords = [0, 0]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                cords[0], cords[1] = cords[0], cords[1] - 3
            elif keys[pygame.K_s]:
                cords[0], cords[1] = cords[0], cords[1] + 3
            elif keys[pygame.K_a]:
                cords[0], cords[1] = cords[0] - 3, cords[1]
            elif keys[pygame.K_d]:
                cords[0], cords[1] = cords[0] + 3, cords[1]
        screen = planet.render(screen)
        screen = player.renderPlayer(screen, cords)
        pygame.display.flip()
        clock.tick(60)
