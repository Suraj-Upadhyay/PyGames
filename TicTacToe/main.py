import pygame

dimensions = (300, 300)
drawx = pygame.image.load("X.png")
drawo = pygame.image.load("O.png")
tictactoe = [['', '', ''], ['', '', ''], ['', '', '']]
tile = [[None, None, None], [None, None, None], [None, None, None]]
is_X = True
i = 0
while i < 3:
    j = 0
    while j < 3:
        tile[i][j] = pygame.Rect(j * 100 + 10, i * 100 + 10, 80, 80)
        j += 1
    i += 1
window = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    color = (0, 0, 0) if is_X else (128, 0, 0)
    window.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Take input.
    mousex, mousey = pygame.mouse.get_pos()
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            if tile[i][j].collidepoint((mousex, mousey)) and pygame.mouse.get_pressed()[0] \
                and tictactoe[i][j] == '':
                tictactoe[i][j] = 'X' if is_X else 'O'
                is_X = not is_X
            j += 1
        i += 1

    # Check for winner.
    if  (tictactoe[0][0] == tictactoe[1][1] and tictactoe[1][1] == tictactoe[2][2] and tictactoe[2][2]) or \
        (tictactoe[0][2] == tictactoe[1][1] and tictactoe[1][1] == tictactoe[2][0] and tictactoe[2][0]) or \
        (tictactoe[0][0] == tictactoe[0][1] and tictactoe[0][1] == tictactoe[0][2] and tictactoe[0][2]) or \
        (tictactoe[1][0] == tictactoe[1][1] and tictactoe[1][1] == tictactoe[1][2] and tictactoe[1][2]) or \
        (tictactoe[2][0] == tictactoe[2][1] and tictactoe[2][1] == tictactoe[2][2] and tictactoe[2][2]) or \
        (tictactoe[0][0] == tictactoe[1][0] and tictactoe[1][0] == tictactoe[2][0] and tictactoe[2][0]) or \
        (tictactoe[0][1] == tictactoe[1][1] and tictactoe[1][1] == tictactoe[2][1] and tictactoe[2][1]) or \
        (tictactoe[0][2] == tictactoe[1][2] and tictactoe[1][2] == tictactoe[2][2] and tictactoe[2][2]):
        run = False
        player = 'O' if is_X else 'X'
        print(player, "won")

    # Display everything.
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            pygame.draw.rect(window, (255, 255, 255), tile[i][j])
            if tictactoe[i][j] == 'X':
                window.blit(drawx, tile[i][j])
            elif tictactoe[i][j] == 'O':
                window.blit(drawo, tile[i][j])
            j += 1
        i += 1
    pygame.display.update()
pygame.quit()
