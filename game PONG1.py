import pygame
import math
import random  # Import modul random
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
FPS = 60
MAX_SCORE = 8   # Skor maksimal untuk menang

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)  # ini untuk warna pinkygame.mixer.music.play()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
clock = pygame.time.Clock()
vec2 = pygame.math.Vector2

# Inisialisasi suara
pygame.mixer.init()
hit_sound = pygame.mixer.Sound('laser.wav')  # ini untuk suara ketika pemain dan musuh mengenai bola
pygame.mixer.music.load('cyberfunk.mp3') # ini untuk suara musik
pygame.mixer.music.play()

# Memuat dan memutar musik latar belakang
pygame.mixer.music.load('cyberfunk.mp3')  # ini untuk suara musik
#background_music = pygame.mixer.music.load('epicsong.mp3') # ini untuk suara musik 2 KALO MAU DI GANTI DGN YG DI ATAS
pygame.mixer.music.play(-1)  # Putar musik secara berulang (-1 untuk loop tak terbatas)

def draw_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    surface_font = font.render(text, True, font_color)
    screen.blit(surface_font, (x, y))

def draw_gradient_text(text, font_size, x, y):
    font = pygame.font.SysFont(None, font_size)
    colors = [RED, ORANGE, YELLOW]
    for i, color in enumerate(colors):
        surface_font = font.render(text, True, color)
        screen.blit(surface_font, (x, y - i * 2))

def draw_centered_gradient_text(text, font_size, y):
    font = pygame.font.SysFont(None, font_size)
    colors = [RED, ORANGE, YELLOW]  # INI UNTUK MERUBAH WARNA PADA TEKS PADA SCREEN AWAL
    text_width, text_height = font.size(text)
    x = (WIDTH - text_width) // 2
    for i, color in enumerate(colors):
        surface_font = font.render(text, True, color)
        screen.blit(surface_font, (x, y - i * 2))

class Particle:
    def __init__(self, x, y):
        self.pos = vec2(x, y)
        self.vel = vec2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.lifetime = random.randint(20, 50)
        self.color = random.choice([RED, ORANGE, YELLOW]) # INI UNTUK MERUBAH WARNA PADA TEKS PADA SCREEN AWAL

    def update(self):
        self.pos += self.vel
        self.lifetime -= 1

    def draw(self):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 3)

class Player:
    def __init__(self, x, y, width, height):
        self.pos = vec2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0
        self.lives = 3  # Tambahkan ini untuk memberikan player tiga kali hidup

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_UP] and self.pos.y > 0:
            self.pos.y -= 10
        if key[K_DOWN] and self.pos.y < HEIGHT - self.height:
            self.pos.y += 10

        self.rect.y = self.pos.y

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Musuh:
    def __init__(self, x, y, width, height):
        self.pos = vec2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_w] and self.pos.y > 0:
            self.pos.y -= 10
        if key[K_s] and self.pos.y < HEIGHT - self.height:
            self.pos.y += 10

        self.rect.y = self.pos.y

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Bola:
    def __init__(self, x, y, radius):
        self.pos = vec2(x, y)
        self.radius = radius
        self.speed = vec2(6, 6) # ini untuk mengatur kecepatan bola
        self.goal = False
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)  # Tambahkan rect untuk deteksi tabrakan

    def update(self, player, musuh):
        if not self.goal:
            if self.pos.x > WIDTH:
                player.score += 1
                self.goal = True
            if self.pos.x < 0:
                musuh.score += 1
                self.goal = True

        if self.goal:
            self.pos.x = WIDTH // 2
            self.pos.y = random.randint(self.radius, HEIGHT - self.radius)  # Reset posisi y secara acak
            self.speed = vec2(-self.speed.x, self.speed.y)
            self.goal = False

        if self.pos.y < self.radius or self.pos.y > HEIGHT - self.radius:
            self.speed.y *= -1

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)  # Perbarui posisi rect
        self.draw()

    def draw(self):
# Gambar bola hijau dan putih
        pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.pos.x), int(self.pos.y)), self.radius, 2)  # Tambahkan garis tepi hijau pada bola

def check_collision(ball, papan):
    cx, cy = ball.pos.x, ball.pos.y

    if ball.pos.x < papan.rect.x:
        cx = papan.rect.x
    elif ball.pos.x > papan.rect.x + papan.rect.width:
        cx = papan.rect.x + papan.rect.width

    if ball.pos.y < papan.rect.y:
        cy = papan.rect.y
    elif ball.pos.y > papan.rect.y + papan.rect.height:
        cy = papan.rect.y + papan.rect.height

    dx = ball.pos.x - cx
    dy = ball.pos.y - cy

    jarak = math.sqrt(dx * dx + dy * dy)

    return jarak <= ball.radius

def start_screen():
    screen.fill(BLACK)
    draw_centered_gradient_text("created by indra", 60, HEIGHT // 2.40 - 50)
    draw_centered_gradient_text("pythonproject", 41, HEIGHT // 2.76 + 50)
    draw_centered_gradient_text("2024", 50, HEIGHT // 2.18 + 50)
    draw_centered_gradient_text("Play now", 35, HEIGHT // 1.80 + 50)
    draw_centered_gradient_text("!!!", 50, HEIGHT // 1.56 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                waiting = False

start_screen()  # Panggil start_screen sebelum loop utama

player = Player(WIDTH - 40, HEIGHT // 2, 20, 100)
musuh = Musuh(20, HEIGHT // 2, 20, 100)
bola = Bola(WIDTH // 2, HEIGHT // 2, 13)

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    screen.fill(BLACK)

    if check_collision(bola, player) or check_collision(bola, musuh):
        bola.speed.x *= -1
        hit_sound.play()  # Mainkan suara ketika bola menyentuh pemain atau musuh

    player.update()
    musuh.update()
    bola.update(player, musuh)

    # Tampilkan nama pemain dan musuh di pojok kiri dan kanan atas dengan warna pink
    draw_text("INDRA =", 26, PINK, 10, 10)
    draw_text("= YOGI", 26, PINK, WIDTH - 86, 10) #SEMAKIN BANYAK SEMAKIN KE KANAN

    # Tampilkan skor di samping nama pemain dan musuh
    draw_text(str(player.score), 30, WHITE, 84, 10)
    draw_text(str(musuh.score), 30, WHITE, WIDTH - 104, 10)#SEMAKIN BANYAK SEMAKIN KE KIRI

    for i in range(HEIGHT // 10):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2, i * 10, 5, 5))

    pygame.display.flip()

    # Cek jika ada pemenang
    if player.score >= MAX_SCORE:
        draw_gradient_text("KALAH", 48, WIDTH - 280, HEIGHT // 2)  # Tampilkan di sisi pemain
        draw_gradient_text("MENANG", 50, 150, HEIGHT // 2)  # Tampilkan di sisi musuh
        pygame.display.flip()
        pygame.time.wait(3000)
        run = False
    elif musuh.score >= MAX_SCORE:
        draw_gradient_text("MENANG", 48, WIDTH - 290, HEIGHT // 2)  # Tampilkan di sisi pemain
        draw_gradient_text("KALAH", 55, 150, HEIGHT // 2)  # Tampilkan di sisi musuh
        pygame.display.flip()
        pygame.time.wait(3000)
        run = False

pygame.quit()
