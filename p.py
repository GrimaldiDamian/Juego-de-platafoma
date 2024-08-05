import pygame

r1 = pygame.Rect(10,10,50,50)
r2 = pygame.Rect(10,50,50,50)

if r2.colliderect(r1):
    print("Esta colisionando")
    if r2.bottom <= r1.top:
        print("Esta colisionando en la parte superior")