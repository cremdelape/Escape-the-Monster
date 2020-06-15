import os
from objects import *
from time import time
import pickle

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('Escape the Monster')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bg = pygame.image.load('Grass Field.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

boat = pygame.sprite.GroupSingle(Boat())
monster = pygame.sprite.GroupSingle(Monster())
rowing = False
playing = True
total_time = 0
begin = time()


def contains(pos):
    if math.hypot((pos[0] - WIDTH // 2), (pos[1] - HEIGHT // 2)) < RADIUS:
        return True


def draw_text(size, text, colour, x=WIDTH // 2, y=HEIGHT // 2):
    font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = font.render(text, 1, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def reset():
    global rowing, playing, begin, total_time, high_score
    high_score = load_highscore()
    rowing = False
    total_time = 0
    begin = time()
    playing = True
    boat.add(Boat())
    monster.add(Monster())


def load_highscore():
    try:
        with open('highscore', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return math.inf


def check_highscore(score, highscore):
    if score < highscore:
        highscore = score
        with open('highscore', 'wb+') as file:
            pickle.dump(highscore, file)
        return True
    else:
        return False


high_score = load_highscore()
while True:
    clock.tick(FPS)
    if playing:
        screen.blit(bg, (0, 0))
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                rowing = not rowing
            if event.button == pygame.BUTTON_RIGHT:
                reset()

    if rowing:
        boat.sprite.move(mouse_pos)

    if playing:
        total_time = round(time() - begin, 1)
        boat.update(mouse_pos)
        monster.update(boat.sprite.pos)
        pygame.draw.circle(screen, BLUE, (WIDTH // 2, HEIGHT // 2), RADIUS)
        # For noobs!
        # pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), BOAT_SPEED * RADIUS // MONSTER_SPEED, 2)
        monster.draw(screen)
        boat.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0), monster.sprite.hitbox, 2)
        # pygame.draw.rect(screen, (0, 255, 0), boat.sprite.hitbox, 2)
        draw_text(32, str(total_time), BLACK, 30, 30)
        draw_text(32, str(high_score), BLACK, 30, 70)

        # Winning Condition
        if not contains(boat.sprite.pos):
            screen.fill((0, 255, 0))
            playing = False
            draw_text(60, 'Land AHO!', WHITE)
            draw_text(50, str(total_time), WHITE, y=(HEIGHT * 3) // 4)
            if check_highscore(total_time, high_score):
                draw_text(50, 'NEW HIGHSCORE!', WHITE, y=HEIGHT // 4)

        # Losing Condition
        if boat.sprite.hitbox.colliderect(monster.sprite.hitbox):
            screen.fill((255, 0, 0))
            playing = False
            draw_text(60, 'YOU WERE EATEN!', WHITE)

    pygame.display.flip()
