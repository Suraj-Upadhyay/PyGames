import pygame
pygame.init()
sudoku = [[0 for i in range(9)] for j in range(9)]
selectedcell = None

dimension = (504, 504)
window = pygame.display.set_mode(dimension)
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if pygame.mouse.get_pressed()[0]:
        mousex, mousey = pygame.mouse.get_pos()
        selectedcell = (mousex // 56, mousey // 56)
    keys = pygame.key.get_pressed()
    if selectedcell:
        if not sudoku[selectedcell[0]][selectedcell[1]]:
            number = 0
            if keys[pygame.K_1]:
                number = 1
            elif keys[pygame.K_2]:
                number = 2
            elif keys[pygame.K_3]:
                number = 3
            elif keys[pygame.K_4]:
                number = 4
            elif keys[pygame.K_5]:
                number = 5
            elif keys[pygame.K_6]:
                number = 6
            elif keys[pygame.K_7]:
                number = 7
            elif keys[pygame.K_8]:
                number = 8
            elif keys[pygame.K_9]:
                number = 9
            sudoku[selectedcell[0]][selectedcell[1]] = number
        # Erase the selected cell.
        elif keys[pygame.K_e]:
            sudoku[selectedcell[0]][selectedcell[1]] = 0
    # Draw everything.
    window.fill((255, 255, 255))
    # Draw light yellow coloured boxes.
    pygame.draw.rect(window, (245, 203, 144), (0, 168, 168, 168))
    pygame.draw.rect(window, (245, 203, 144), (168, 0, 168, 168))
    pygame.draw.rect(window, (245, 203, 144), (336, 168, 168, 168))
    pygame.draw.rect(window, (245, 203, 144), (168, 336, 168, 168))
    # Draw vertical and horizontal lines.
    x = 0
    while x < 504:
        if x % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.rect(window, (0, 0, 0), (x, 0, thickness, 504))
        pygame.draw.rect(window, (0, 0, 0), (0, x, 504, thickness))
        x += 56
    pygame.draw.rect(window, (0, 0, 0), (501, 0, 3, 504))
    pygame.draw.rect(window, (0, 0, 0), (0, 501, 504, 3))
    myfont = pygame.font.SysFont("Times New Roman", 50)
    # Apply shading.
    if selectedcell:
        opacity = 50

        # For 3x3 block.
        block = pygame.Surface((168, 168), pygame.SRCALPHA)
        block.fill((0, 0, 0, opacity))
        blockpos = (selectedcell[0] // 3) * 168, (selectedcell[1] // 3) * 168
        # For the 1x9 horizontal shading.
        hline = pygame.Surface((504, 56), pygame.SRCALPHA)
        hline.fill((0, 0, 0, opacity))
        hlinepos = (0, selectedcell[1] * 56)
        # For the 1x9 vertical shading.
        vline = pygame.Surface((56, 504), pygame.SRCALPHA)
        vline.fill((0, 0, 0, opacity))
        vlinepos = (selectedcell[0] * 56, 0)

        window.blit(block, blockpos)
        window.blit(hline, hlinepos)
        window.blit(vline, vlinepos)
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            number = sudoku[i][j]
            if number:
                label = myfont.render(str(number), 4, (0, 0, 0))
                window.blit(label, (i * 56 + 15, j * 56))
            j += 1
        i += 1
    pygame.display.update()
pygame.quit()
