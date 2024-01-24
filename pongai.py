import pygame
import random

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 60

# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect

# Ball class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = 6 * speed  # Hızı iki katına çıkar
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.firstTime = 1

    def reset(self):
        self.posx = random.randint(self.radius, WIDTH - self.radius)
        self.posy = random.randint(self.radius, HEIGHT - self.radius)
        self.xFac = random.choice([1, -1])  # Rastgele başlangıç yönü
        self.yFac = random.choice([1, -1])  # Rastgele başlangıç yönü
        self.firstTime = 1

    def display(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, 2 * self.radius, 2 * self.radius)

# AI class
class AI:
    def __init__(self, striker, ball):
        self.striker = striker
        self.ball = ball

    def update(self):
        # Her AI'nın aynı anda aynı hareketi yapmaması için rastgele bir yön seç
        yFac = random.choice([-1, 1])
        self.striker.update(yFac)

def simulate_game(simulation_count):
    geek1_total_score = 0
    geek2_total_score = 0
    score_diff_list = []

    for _ in range(simulation_count):
        geek1 = Striker(20, 0, 10, 100, 10, GREEN)
        geek2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
        ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 2, WHITE)
        ai_player1 = AI(geek1, ball)
        ai_player2 = AI(geek2, ball)

        listOfGeeks = [geek1, geek2]
        geek1Score, geek2Score = 0, 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for geek in listOfGeeks:
                if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                    ball.hit()

            ai_player1.update()
            ai_player2.update()
            point = ball.update()

            if point == -1:
                geek1Score += 1
            elif point == 1:
                geek2Score += 1

            if point:
                print(f"Raunt Bitti - Skor Durumu: {geek1Score} - {geek2Score}")
                ball.reset()

            if geek1Score >= 100 or geek2Score >= 100:
                print(f"Oyun Bitti - Sonuç: {geek1Score} - {geek2Score}")
                break

        geek1_total_score += geek1Score
        geek2_total_score += geek2Score
        score_diff_list.append(geek2Score - geek1Score)

    avg_score_diff = sum(score_diff_list) / simulation_count
    print(f"Ortalama Skor Farkı: {avg_score_diff:.2f}")

    # Oyun sonuçlarını ve ortalama skor farkını results.txt adlı bir dosyaya yaz
    with open('results.txt', 'w') as file:
        file.write(f"Toplam Geek1 Skoru: {geek1_total_score}\n")
        file.write(f"Toplam Geek2 Skoru: {geek2_total_score}\n")
        file.write(f"Ortalama Skor Farkı: {avg_score_diff:.2f}")


# Kullanıcıdan simülasyon sayısını al
simulation_count = int(input("Oyunu kaç kez simüle etmek istersiniz? "))
simulate_game(simulation_count)
pygame.quit()
