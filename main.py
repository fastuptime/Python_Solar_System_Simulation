import pygame
import math

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Güneş Sistemi Simülasyonu")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SUN_COLOR = (255, 255, 0)
PLANET_COLORS = {
    "Mercury": (169, 169, 169),
    "Venus": (255, 223, 0),
    "Earth": (0, 0, 255),
    "Mars": (255, 69, 0),
    "Jupiter": (255, 165, 0),
    "Saturn": (210, 180, 140),
    "Uranus": (0, 255, 255),
    "Neptune": (0, 0, 139)
}

class Planet:
    def __init__(self, name, distance, radius, color, orbital_period):
        self.name = name
        self.distance = distance
        self.radius = radius
        self.color = color
        self.orbital_period = orbital_period
        self.angle = 0
        self.orbit = []
        self.orbit_count = 0

    def update_position(self, dt):
        self.angle += dt * 2 * math.pi / self.orbital_period
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
            self.orbit_count += 1
            self.orbit = []
        self.x = width / 2 + self.distance * math.cos(self.angle)
        self.y = height / 2 + self.distance * math.sin(self.angle)
        self.orbit.append((self.x, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for point in self.orbit:
            pygame.draw.circle(screen, self.color, (int(point[0]), int(point[1])), 1)

    def draw_info(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.name}: Tur {self.orbit_count}", True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y - self.radius - 20))
        screen.blit(text, text_rect)

planets = [
    Planet("Merkül", 60, 4, PLANET_COLORS["Mercury"], 88),
    Planet("Venüs", 108, 7, PLANET_COLORS["Venus"], 225),
    Planet("Dünya", 150, 8, PLANET_COLORS["Earth"], 365),
    Planet("Mars", 228, 6, PLANET_COLORS["Mars"], 687),
    Planet("Jupiter", 778, 14, PLANET_COLORS["Jupiter"], 4333),
    Planet("Satürn", 1427, 12, PLANET_COLORS["Saturn"], 10759),
    Planet("Uranüs", 2871, 10, PLANET_COLORS["Uranus"], 30685),
    Planet("Neptün", 4497, 10, PLANET_COLORS["Neptune"], 60190),
    # Planet("Pluto", 5900, 3, (255, 255, 255), 90520) AH BE PLÜTO
]

running = True
clock = pygame.time.Clock()
scale = 0.02 # 1 gün = 0.02 saniye


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    pygame.draw.circle(screen, SUN_COLOR, (width // 2, height // 2), 30)

    for planet in planets:
        planet.update_position(clock.get_time() * scale)
        planet.draw(screen)

    font = pygame.font.Font(None, 24)
    y_offset = 10
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for planet in planets:
        if math.sqrt((planet.x - mouse_x) ** 2 + (planet.y - mouse_y) ** 2) < planet.radius:
            planet.draw_info(screen)

        info = f"{planet.name}: Mesafe={planet.distance} AU, 1 Tur = {planet.orbital_period} gün, Tur = {planet.orbit_count}, {planet.name}'in 1 Turu = {planet.orbital_period} gün"
        text = font.render(info, True, WHITE)
        screen.blit(text, (10, y_offset))
        y_offset += 30

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
