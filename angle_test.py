import pygame

P1 = 1, 0
P2 = 5, 0

v1 = pygame.math.Vector2(P1)
v2 = pygame.math.Vector2(P2)

angle1 = v1.angle_to(v2)
angle2 = v2.angle_to(v1)

print(v1, v2, angle1)
print(v2, v1, angle2)
