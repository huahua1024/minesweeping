import pygame
from pygame.locals import *
from random import randint
# import pprint

SCREEN_SIZE = (800, 600)
GRID_SIZE = 30
TIPS_FONT_SIZE = 20
BOMB_NUM_SIZE = 16
OFFSET = 10  # offset to original point
ROW = 9     # max num in x-axis
COLUMN = 9  # max num in y-axis
BOMBS = 10   # bombs number in mine grid

# color definition
BLACK_COLOR = (0, 0, 0)
GRID_LINE_COLOR = (0, 0, 255)
DEFAULT_COLOR = (0, 255, 255)
OVER_COLOR = (255, 200, 90)
FLAG_COLOR = (200, 100, 200)
BOMB_COLOR = (255, 0, 0)
BOMB_NUM_COLOR = (155, 55, 25)
TIPS_COLOR = (255, 255, 100)
OPEN_COLOR = (255, 200, 90)

around_index = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


# initial mine dictionary, with given number bombs in random position
def MineInit(row, column, bombs_num):
    # initial mine dictionary , with no bombs in it.
    # has a trick:around the grid set extra circle, set all the value to 0
    mine = {}
    for y in range(-1, column+1):
        for x in range(-1, row+1):
            mine.setdefault((x, y), {'bomb': 0, 'flag': 0, 'bomb_around': 0})
    # given number bombs in random coordinate
    bombs = []
    while len(bombs) < bombs_num:
        coord = (randint(0, row-1), randint(0, column-1))
        if coord not in bombs:
            bombs.append(coord)
    # set the value of the given coordinate position in mine dictionary to 'bomb':1, means that it contain a bomb
    for b in bombs:
        mine[b]['bomb'] = 1
        # mine[b]['flag'] = 1
        # every grid around the bomb grid set its 'bomb_around' increase one(total 8 grid should change)
        for idx in around_index:
            mine[(b[0]+idx[0], b[1]+idx[1])]['bomb_around'] += 1
    # return mine dictionary
    return mine


# initial the mine board, surface: where to draw; row: max row line in x-axis; column: max column line in y-axis
def GameInit(surface, row, column, bombs_num):
    surface.fill(BLACK_COLOR)
    # draw y-axis lines
    for x in range(row+1):
        p1 = (x*(GRID_SIZE+1)+OFFSET, 0+OFFSET)
        p2 = (x*(GRID_SIZE+1)+OFFSET, column*(GRID_SIZE+1)+OFFSET)
        pygame.draw.line(surface, GRID_LINE_COLOR, p1, p2)
        # print('column: ', p1, '->', p2)
    # draw x-axis lines
    for y in range(column+1):
        p1 = (0 + OFFSET, y * (GRID_SIZE+1) + OFFSET)
        p2 = (row * (GRID_SIZE+1) + OFFSET, y * (GRID_SIZE+1) + OFFSET)
        pygame.draw.line(surface, GRID_LINE_COLOR, p1, p2)
        # print('row: ', p1, '->', p2)
    mine_grid = MineInit(row, column, bombs_num)

    # draw all the mine grids,
    # k is mine_grid's key,means a coordinate; v is mine_grid's value, is a dict too. v.key 'bomb' means a bomb or not
    for k, v in mine_grid.items():
        # don't draw the extra circle around the mine grids
        if -1 < k[0] < row and -1 < k[1] < column:
            draw_rect (surface, DEFAULT_COLOR, k)
            # if v['bomb'] == 1:
            #     draw_rect(surface, BOMB_COLOR, k)
            # else:
            #     draw_rect(surface, DEFAULT_COLOR, k)

    # draw the tips text
    txt = '\'R\': restart'
    pos = (OFFSET*4, column*(GRID_SIZE+1) + OFFSET*4)
    write_label(surface, txt, pos, TIPS_COLOR, TIPS_FONT_SIZE)
    txt = '\'S\': show bombs'
    pos = (OFFSET * 4, column * (GRID_SIZE + 1) + OFFSET * 4 + TIPS_FONT_SIZE*1)
    write_label(surface, txt, pos, TIPS_COLOR, TIPS_FONT_SIZE)
    txt = '\'H\': hide bombs'
    pos = (OFFSET * 4, column * (GRID_SIZE + 1) + OFFSET * 4 + TIPS_FONT_SIZE * 2)
    write_label(surface, txt, pos, TIPS_COLOR, TIPS_FONT_SIZE)

    # draw game information
    draw_info_window (surface, BOMBS, 0)

    # update the game board and return the mine_grid
    pygame.display.update()
    return mine_grid


def draw_info_window(surface, bombs, time):
    # ps = Rect(SCREEN_SIZE[0]-150, OFFSET, 140, 90)
    ps = Rect (ROW*(GRID_SIZE+1) + 50, OFFSET, 140, 90)
    pygame.draw.rect(surface, GRID_LINE_COLOR, ps, 2)

    cls_ps = (ps[0]+5, ps[1]+5, 130, 80)
    pygame.draw.rect (surface, BLACK_COLOR, cls_ps)
    txt_bombs = 'bomb: ' + str(bombs)
    txt_time = 'time: ' + str(time)
    write_label (surface, txt_bombs, (ps[0]+OFFSET, ps[1]+OFFSET), TIPS_COLOR, TIPS_FONT_SIZE)
    write_label (surface, txt_time, (ps[0]+OFFSET, ps[1]+OFFSET+TIPS_FONT_SIZE*2), TIPS_COLOR, TIPS_FONT_SIZE)
    pygame.display.update()

    # print(bombs)
    # print(time)


# write label in setting position
def write_label(surface, message, pos, message_color, size):
    #  message txt render
    font = pygame.font.SysFont("simsunnsimsun", size, 0)
    label = font.render(message, True, message_color)
    surface.blit(label, pos)


# draw rect with given color
def draw_rect(surface, draw_color, coord):
    x = coord[0] * (GRID_SIZE+1) + OFFSET
    y = coord[1] * (GRID_SIZE+1) + OFFSET
    pos = (x + 1, y + 1)
    shape = (GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, draw_color, Rect(pos, shape))
    # print(pos)


# 判断鼠标是否经过游戏棋盘的某个坐标，返回此坐标
def is_over(point):
    # point 是鼠标经过的点的坐标值
    point_x, point_y = point
    point_x -= OFFSET
    point_y -= OFFSET

    # if the point in game board, return its coordinate
    if (0 < point_x < ROW*(GRID_SIZE+1)) and (0 < point_y < COLUMN*(GRID_SIZE+1)):
        in_x = int(point_x/(GRID_SIZE+1))
        in_y = int(point_y/(GRID_SIZE+1))
        coord = (in_x, in_y)
        return coord
    else:
        return None


# when mouse moves action, 鼠标经过棋盘时，经过的格子会变颜色，离开原来的格子时，原来格子变回默认颜色
def mouse_move(surface, pos, pre_coord, mine_grid):
    over_coord = is_over(pos)
    # 当前经过坐标在棋盘内， 则根据当前格子是否已经翻开决定是否改变颜色
    if over_coord:  # in mine_grid.keys():
        if over_coord != pre_coord:
            if mine_grid[over_coord]['flag'] == 0:
                draw_rect(surface, OVER_COLOR, over_coord)
            if (pre_coord is not None) and (mine_grid[pre_coord]['flag'] == 0):
                draw_rect(surface, DEFAULT_COLOR, pre_coord)
    # 离开棋盘，恢复原来着色
    else:
        if (pre_coord is not None) and (mine_grid[pre_coord]['flag'] == 0):
            draw_rect(surface, DEFAULT_COLOR, pre_coord)

    pygame.display.update()
    return over_coord


def show_bombs(surface, mine_grid):
    for k, v in mine_grid.items ():
        # don't draw the extra circle around the mine grids
        if -1 < k[0] < ROW and -1 < k[1] < COLUMN:
            if v['bomb'] == 1:
                draw_rect (surface, BOMB_COLOR, k)
    pygame.display.update()


def hide_bombs(surface, mine_grid):
    for k, v in mine_grid.items ():
        # don't draw the extra circle around the mine grids
        if -1 < k[0] < ROW and -1 < k[1] < COLUMN:
            if v['bomb'] == 1:
                draw_rect (surface, DEFAULT_COLOR, k)
    pygame.display.update ()


def mouse_left_press(surface, coord, mine_grid):
    if coord:
        if mine_grid[coord]['flag'] == 0:   # 是否是未打开过的格子？
            if mine_grid[coord]['bomb'] == 1:   # this grid has a bomb, return 'game over'
                print('game over')
                return 'game over'
            else:
                grid_open(surface, coord, mine_grid)  # open itself
                pygame.display.update()
                return 'open ok'
    else:
        return None


def grid_open(surface, coord, mine_grid):
    # 如果坐标在盘内，且未打开过， 就打开此格，且判断它是否周围没有雷，是就再翻开周边八个格子。
    if -1 < coord[0] < ROW and -1 < coord[1] < COLUMN and mine_grid[coord]['flag'] == 0:
        mine_grid[coord]['flag'] = 3
        draw_rect(surface, OPEN_COLOR, coord)
        write_numbers(surface, coord, mine_grid)
        if mine_grid[coord]['bomb_around'] == 0:
            for idx in around_index:
                grid_open(surface, (coord[0] + idx[0], coord[1] + idx[1]), mine_grid)
    else:
        return None


def write_numbers(surface, coord, mine_grid):
    if mine_grid[coord]['bomb_around'] != 0:
        font = pygame.font.SysFont("arial", BOMB_NUM_SIZE)
        txt = str(mine_grid[coord]['bomb_around'])
        p1 = coord[0] * (GRID_SIZE + 1) + OFFSET + 15
        p2 = coord[1] * (GRID_SIZE + 1) + OFFSET + 10
        pos = (p1, p2)
        label = font.render(txt, True, BOMB_NUM_COLOR)
        surface.blit(label, pos)


def write_flags(surface, coord, mine_grid):
    if mine_grid[coord]['flag'] == 0:
        txt = ''
        write_color = OVER_COLOR
    if mine_grid[coord]['flag'] == 1:
        txt = '*'
        write_color = FLAG_COLOR
    if mine_grid[coord]['flag'] == 2:
        txt = '?'
        write_color = FLAG_COLOR

    draw_rect (surface, write_color, coord)
    font = pygame.font.SysFont("arial", BOMB_NUM_SIZE)
    p1 = coord[0] * (GRID_SIZE + 1) + OFFSET + 15
    p2 = coord[1] * (GRID_SIZE + 1) + OFFSET + 10
    pos = (p1, p2)
    label = font.render(txt, True, BOMB_COLOR)
    surface.blit(label, pos)
    pygame.display.update()


def mouse_right_press(surface, coord, mine_grid):
    if coord and mine_grid[coord]['flag'] != 3:
        if mine_grid[coord]['flag'] == 0:   # 是否是未打开过的格子？
            mine_grid[coord]['flag'] = 1
            return_info = 'bomb_minus'
        elif mine_grid[coord]['flag'] == 1:   # 是否是格子显示小旗子？
            mine_grid[coord]['flag'] = 2
            return_info = 'bomb_add'
        elif mine_grid[coord]['flag'] == 2:   # 是否是格子显示'?'？
            mine_grid[coord]['flag'] = 0
            return_info = None

        write_flags (surface, coord, mine_grid)
        return return_info
    else:
        return None


def mouse_left_right_press():
    pass


def GameOver(surface, mine_grid):
    show_bombs(surface, mine_grid)
    txt = 'Game Over!!!'
    write_label(surface, txt, (SCREEN_SIZE[0]/5, SCREEN_SIZE[1]/3), (0, 0, 255), 80)
    pygame.display.update()


def GameWin(surface, mine_grid):
    bombs_found = 0
    for k, v in mine_grid.items():
        if v['bomb'] and v['flag'] == 1:
            bombs_found += 1

    if bombs_found == BOMBS:
        txt = 'You Won!!!'
        write_label (surface, txt, (SCREEN_SIZE[0] / 5, SCREEN_SIZE[1] / 3), (0, 0, 255), 80)
        pygame.display.update ()
        return 'game win'
    else:
        return None


def run():
    # initial the game screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    mine_grid = GameInit(screen, ROW, COLUMN, BOMBS)
    pre_coord = None
    clock = pygame.time.Clock ()
    time_passed_seconds = 0
    pre_seconds = 0
    bomb_remain = BOMBS
    game_status = 'begin'

    while True:
        for event in pygame.event.get ():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        mine_grid = GameInit (screen, ROW, COLUMN, BOMBS)
                        pre_seconds = 0
                        time_passed_seconds = 0
                        time_passed = clock.tick()
                        bomb_remain = BOMBS
                        game_status = 'begin'
        if game_status == 'game over':
            GameOver(screen, mine_grid)
            game_status = 'waiting'

        if game_status == 'begin':
            # main game loop
            while True:
                time_passed = clock.tick ()
                time_passed_seconds += time_passed / 1000
                if int(time_passed_seconds) != pre_seconds:
                    draw_info_window (screen, bomb_remain, int(time_passed_seconds))
                    pre_seconds = int(time_passed_seconds)

                if game_status == 'game over':
                    break

                game_status = GameWin (screen, mine_grid)
                if game_status == 'game win':
                    break

                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            mine_grid = GameInit(screen, ROW, COLUMN, BOMBS)
                            time_passed_seconds = 0
                            pre_seconds = 0
                            bomb_remain = BOMBS
                        elif event.key == K_s:
                            show_bombs(screen, mine_grid)
                        elif event.key == K_h:
                            hide_bombs(screen, mine_grid)

                    if event.type == MOUSEMOTION:
                        over_coord = mouse_move(screen, event.pos, pre_coord, mine_grid)
                        if over_coord != pre_coord:
                            pre_coord = over_coord
                    if event.type == MOUSEBUTTONDOWN:
                        click_coord = is_over (event.pos)
                        if event.button == 1:
                            # print('mouse left press')
                            game_status = mouse_left_press(screen, click_coord, mine_grid)
                        elif event.button == 3:
                            print ('mouse right press')
                            bomb_remain_info = mouse_right_press(screen, click_coord, mine_grid)
                            if bomb_remain_info == 'bomb_minus':
                                    bomb_remain -= 1
                            elif bomb_remain_info == 'bomb_add':
                                    bomb_remain += 1


if __name__ == '__main__':
    run()
