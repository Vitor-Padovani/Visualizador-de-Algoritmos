import pygame
import random
import math
import os
pygame.init()

PATH = os.getcwd().replace('\\', '/')

img = pygame.image.load('./img/icon.png')
pygame.display.set_icon(img)

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = BLACK

    FONT = pygame.font.SysFont('consolas', 20)
    LARGE_FONT = pygame.font.SysFont('consolas', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visualizador de Algoritmo")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascendente' if ascending else 'Descendente'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, ( (draw_info.width - title.get_width() )/ 2, 10))

    controls = draw_info.FONT.render('R - Resetar | ESPAÇO - Ordenar | A - Ascendente | D - Descendente', 1, draw_info.WHITE)
    draw_info.window.blit(controls, ( (draw_info.width - controls.get_width() )/ 2, 50))

    sorting = draw_info.FONT.render('I - Insertion Sort | B - Bubble Sort | C - Comb Sort', 1, draw_info.WHITE)
    draw_info.window.blit(sorting, ( (draw_info.width - sorting.get_width() )/ 2, 80))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        hue = int(math.floor(val * 1.2))
        color = (hue, hue, 255 - hue)

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def comb_sort(draw_info, ascending=True):
    lst = draw_info.lst
    gap = math.floor(len(lst) / 1.3)
    i = 0

    while gap > 0 and i != len(lst) - 1:
        i = 0

        while i + gap < len(lst):

            if (lst[i] > lst[i+gap] and ascending) or (lst[i] < lst[i+gap] and not ascending):
                lst[i], lst[i+gap] = lst[i+gap], lst[i]

            draw_list(draw_info, {i: draw_info.GREEN, i+gap: draw_info.RED}, True)

            i += 1
            yield True
        
        gap = math.floor(gap / 1.3)

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 200

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = 'Bubble Sort'
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(f'{PATH}/SFX/resolve.mp3')
                pygame.mixer.music.play()
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                pygame.mixer.music.stop()
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                pygame.mixer.music.load(f'{PATH}/SFX/expect.mp3')
                pygame.mixer.music.play()
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = 'Insertion Sort'
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = 'Bubble Sort'
            elif event.key == pygame.K_c and not sorting:
                sorting_algorithm = comb_sort
                sorting_algo_name = 'Comb Sort'


    pygame.quit()

if __name__ == "__main__":
    main()
