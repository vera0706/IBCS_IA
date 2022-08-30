import pygame, sys
from PlayerClass import Player

# from UserInterface import UserInterface
menu_clock = pygame.time.Clock()
clock = pygame.time.Clock()
pygame.display.set_caption('Colour!')

pygame.init()

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((320, 180))
main_display = pygame.Surface((320, 180))
options_display = pygame.Surface((320, 180))
settings_display = pygame.Surface((320, 180))

# player init
player = Player()

# load tile images here

floor_tile = pygame.image.load("floor.png").convert_alpha()
TILE_SIZE = 16


class Level:
    # pass map_file as a string that is the file path of the map
    def __init__(self, map):
        self.map_file = map
        self.map_text = []
        self.map_tiles = []
        self.map_rects = []
        self.map_colliders = []

    def load_map(self):
        f = open(self.map_file, "r")
        self.map_text = f.read()
        f.close()
        self.map_text = self.map_text.split('\n')
        for line in self.map_text:
            self.map_tiles.append(list(line))

    def draw_map(self, display_surface):
        self.map_rects = []
        y = 0
        for line in self.map_tiles:
            x = 0
            for tile in line:
                if tile == "1":
                    display_surface.blit(floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
                if tile != "0":
                    self.map_rects.append(pygame.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                x += 1
            y += 1

    def test_map_collision(self, rect):
        self.map_colliders = []
        for tile in self.map_rects:
            if pygame.Rect.colliderect(rect, tile):
                self.map_colliders.append(tile)

    def map_collision(self, rect, movement):
        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        rect.x += movement[0]
        self.test_map_collision(rect)
        for tile in self.map_colliders:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        self.test_map_collision(rect)
        for tile in self.map_colliders:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types


# levels
level_one = Level('map.txt')
level_one.load_map()

player.becomes_colourful()


# run game
def run_game():
    anim_count = 1
    idle_count = 0
    while True:
        display.fill((146, 244, 255))
        player.update(anim_count, idle_count)
        level_one.draw_map(display)

        player.rect, collisions = level_one.map_collision(player.rect, player.player_movement)
        if collisions['top']:
            player.player_y_momentum = 2
            player.is_jumping = False
            player.is_falling = True
        if collisions['bottom']:
            player.player_y_momentum = 0
            player.air_timer = 0
            player.is_falling = False
        else:
            player.air_timer += 1

        player.draw(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player.is_idle = False
                if keys[pygame.K_LSHIFT] and player.is_colourful:
                    player.is_changing_colour = True
                if event.key == pygame.K_z:
                    if player.air_timer < 6:
                        player.player_y_momentum = -7
                        player.is_jumping = True
                if not player.is_changing_colour:
                    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]: # event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                        player.is_idle = True
                        player.moving_right, player.moving_left = False, False
                    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                        player.moving_right = True
                        player.moving_left = False
                        player.is_idle = False
                        player.facing_right, player.facing_left = True, False
                    elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                        player.moving_left = True
                        player.moving_right = False
                        player.is_idle = False
                        player.facing_left, player.facing_right = True, False
                else:
                    player.moving_left, player.moving_right = False, False
                    if event.key == pygame.K_LEFT:
                        if player.colour_index >= 2:
                            player.colour_index = 0
                        else:
                            player.colour_index += 1
                        player.change_colour()
                        idle_count = 0
                    elif event.key == pygame.K_RIGHT:
                        if player.colour_index <= 0:
                            player.colour_index = 2
                        else:
                            player.colour_index -= 1
                        player.change_colour()
                        idle_count = 0
                if event.key == pygame.K_ESCAPE:
                    options_menu()
            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                player.is_idle = True
                if event.key == pygame.K_RIGHT:
                    player.moving_right = False
                    if keys[pygame.K_LEFT]:
                        player.moving_left = True
                        player.facing_left, player.facing_right = True, False
                        player.is_idle = False
                    else:
                        player.moving_left = False
                        player.facing_right, player.facing_left = True, False
                if event.key == pygame.K_LEFT:
                    player.moving_left = False
                    if keys[pygame.K_RIGHT]:
                        player.moving_right = True
                        player.facing_right, player.facing_left = True, False
                        player.is_idle = False
                    else:
                        player.moving_right = False
                        player.facing_left, player.facing_right = True, False
                        player.is_idle = True
                if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                    player.is_idle = True
                    player.moving_left, player.moving_right = False
                if event.key == pygame.K_z:
                    player.is_jumping = False
                    if collisions['bottom']:
                        player.is_idle = True
                        player.is_falling = False
                        player.is_jumping = False
                    else:
                        player.is_idle = False
                if event.key == pygame.K_LSHIFT and player.is_colourful:
                    player.is_changing_colour = False

        if player.player_y_momentum > 1.21:
            player.is_jumping = False
            player.is_falling = True
        elif player.player_y_momentum > 0:
            player.is_jumping = False
            if not player.moving_left and not player.moving_right:
                player.is_idle = True

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)
        if anim_count >= 5:
            anim_count = 0
        anim_count += 1
        if not player.is_idle:
            idle_count = 0
        elif player.is_idle:
            if idle_count <= 240:
                idle_count += 1



def main_menu():
    click = False
    play_button = pygame.image.load('main_menu_buttons/play_button.png').convert_alpha()
    play_button_rect = pygame.Rect(100, 60, play_button.get_width(), play_button.get_height())
    quit_button = pygame.image.load('main_menu_buttons/quit_button.png').convert_alpha()
    quit_button_rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        main_display.fill('black')

        m_x, m_y = pygame.mouse.get_pos()

        main_display.blit(play_button, (play_button_rect.x, play_button_rect.y))
        main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        play_button_rect_scaled = pygame.Rect(400, 240, 400, 200)
        quit_button_rect_scaled = pygame.Rect(400, 480, 400, 200)
        if play_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                run_game()
            main_display.fill('black')
            main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
            main_display.blit(play_button, (play_button_rect.x, play_button_rect.y - 5))
        elif quit_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                pygame.quit()
                sys.exit()
            main_display.fill('black')
            main_display.blit(play_button, (play_button_rect.x, play_button_rect.y))
            main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y - 5))

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(main_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)


def options_menu():
    click = False
    resume_button = pygame.image.load('options_buttons/resume_button.png').convert_alpha()
    resume_button_rect = pygame.Rect(100, 60, resume_button.get_width(), resume_button.get_height())
    settings_button = pygame.image.load('options_buttons/settings_button.png').convert_alpha()
    settings_button_rect = pygame.Rect(100, 80, settings_button.get_width(), settings_button.get_height())
    exit_to_menu_button = pygame.image.load('options_buttons/exit_to_menu_button.png').convert_alpha()
    exit_to_menu_button_rect = pygame.Rect(100, 100, exit_to_menu_button.get_width(), exit_to_menu_button.get_height())
    quit_button = pygame.image.load('options_buttons/quit_button.png').convert_alpha()
    quit_button_rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        options_display.fill('black')
        m_x, m_y = pygame.mouse.get_pos()
        options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
        options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
        options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
        options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        if resume_button_rect.collidepoint((m_x, m_y)):
            if click:
                break
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y-5))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif exit_to_menu_button_rect.collidepoint((m_x, m_y)):
            if click:
                main_menu()
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y-5))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif quit_button_rect.collidepoint((m_x, m_y)):
            if click:
                pygame.quit()
                sys.exit()
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y-5))
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(options_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)

'''

def settings():
    click = False
    while True:
elif settings_button_rect.collidepoint((m_x, m_y)):
            if click:
                settings()
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y-5))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

'''

main_menu()