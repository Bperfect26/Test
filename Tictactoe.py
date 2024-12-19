import pygame
pygame.init()
screen = pygame.display.set_mode((255,255))
WHITE = (255,255,255)
GREEN = (100,255,100)
RED = (255,100,100)
size = 75
width = size
height = size
margin = 7.25
grid = []
colortemp = True

# Function to check for win condition
def check_win(grid):
    # Check rows and columns
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != 0: # Rows
            return grid[i][0]
        if grid[0][i] == grid[1][i] == grid[2][i] != 0: # Columns
            return grid[0][i]
    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != 0: # Diagonal from top-left to bottom-right
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != 0: # Diagonal from top-right to bottom-left
        return grid[0][2]
    return 0  # No winner yet
def reset_game():
    global grid, colortemp
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    colortemp = True
# Loop for each row
for row in range(3):
    # For each row, create a list that will represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(3):
        # Add a the number zero to the current row
        grid[row].append(0)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0] // (width + margin)
            y = pos[1] // (height + margin)
            if grid[int(y)][int(x )] == 0 and colortemp == True:
                grid[int(y)][int(x)] = 1
                colortemp = False
            elif grid[int(y)][int(x )] == 0 and colortemp == False:
                grid[int(y)][int(x)] = 2
                colortemp = True
            winner = check_win(grid)
            if winner != 0:
                print("Player", winner, "wins!")
                reset_game()
    for column in range(3):
        for row in range(3):
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(screen,color,((margin + width) * column + margin,(margin + height) * row + margin,width,height))
    pygame.display.update()