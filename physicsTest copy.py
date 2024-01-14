import pygame
from entity import Player as p
from allEntities import *
import colorGradient as cg
import collisionHandler as ch

pygame.init()
windowDim = (500, 500)

win = pygame.display.set_mode(windowDim)
pygame.display.set_caption("Sandevistan!!!")

allEntities = [david]
environment = [bound1, bound2, bound3, bound4]

run = True

while run:

    win.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    userInput = pygame.key.get_pressed()

    if userInput[pygame.K_a]:
        david.force(p.LEFT, david.dex)
    if userInput[pygame.K_d]:
        david.force(p.RIGHT, david.dex)
    if userInput[pygame.K_w]:
        david.force(p.UP, david.dex)
    if userInput[pygame.K_s]:
        david.force(p.DOWN, david.dex)

    for entity in allEntities:
        ch.resolveMotion(entity, environment)
    
    for entity in allEntities:
        pygame.draw.circle(win, cg.WHITE, entity.position, 15)

    for surface in environment:
        pygame.draw.line(win, cg.HOT_PINK, surface.edge1, surface.edge2, 3)

    pygame.time.delay(32)

    pygame.display.update()