import pygame
import sys

pygame.init()

#constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH//8

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

#create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

#Chess piece class
class ChessPiece:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

#Initialize the chess board
board = [[None for _ in range(8)] for _ in range(8)]

#current player
currentPlayer = "white"
selectedPiece = None
selectedPos = None

def init_board():
    
    for col in range(8):
        #Pawns
        board[1][col] = ChessPiece('black', 'pawn','images/b_pawn.png')
        board[6][col] = ChessPiece('white', 'pawn','images/w_pawn.png')
    
    #Rooks
    board[0][0] = board[0][7] = ChessPiece('black','rook','images/b_rook.png')
    board[7][0] = board[7][7] = ChessPiece('white','rook','images/w_rook.png')

    #Knights
    board[0][1] = board[0][6] = ChessPiece('black','knight','images/b_knight.png')
    board[7][1] = board[7][6] = ChessPiece('white','knight','images/w_knight.png')

    #Bishops
    board[0][2] = board[0][5] = ChessPiece('black','bishop','images/b_bishop.png')
    board[7][2] = board[7][5] = ChessPiece('white','bishop','images/w_bishop.png')

    #Queens
    board[0][3] = ChessPiece('black','queen','images/b_queen.png')
    board[7][3] = ChessPiece('white','queen','images/w_queen.png')

    #Kings
    board[0][4] = ChessPiece('black','king','images/b_king.png')
    board[7][4] = ChessPiece('white','king','images/w_king.png')

#function to draw board
def draw_board():
    screen.fill((0,0,0))
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    if selectedPos:
        pygame.draw.rect(screen, YELLOW, (selectedPos[1]*SQUARE_SIZE, selectedPos[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#function to draw piece
def draw_piece():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col*SQUARE_SIZE, row*SQUARE_SIZE))

#function to get valid moves for a piece
def get_valid_moves(piece, row, col):
    moves = []
    if piece.type == 'pawn':
        direction = -1 if piece.color == 'white' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row+direction, col))
            if(piece.color == 'white' and row == 6) or (piece.color == 'black' and row == 1):
                if board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))

        #dc = diagonal column direction
        for dc in [-1,1]:
            if 0 <= row + direction < 8 and 0 <= col + dc < 8:
                if board[row + direction][col + dc] and board[row + direction][col + dc].color != piece.color:
                    moves.append((row + direction, col + dc))

    elif piece.type == 'rook':
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c= r + dr, c + dc

    elif piece.type == 'knight':
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                moves.append((r, c))

    elif piece.type == 'bishop':
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif piece.type == 'queen':
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif piece.type == 'king':
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                
                if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                    moves.append((r,c))

    return moves

#function to check if the king is in check
def is_check(color):
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c].color == color and board[r][c].type == 'king':
                king_pos = (r, c)
                break
        if king_pos:
            break

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color != color:
                if king_pos in get_valid_moves(piece, r, c):
                    return True
    return False

##function to check for checkmate
def is_game_over():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color == currentPlayer:
                valid_moves = get_valid_moves(piece, r, c)
                
                for move in valid_moves:
                    #try the move
                    temp = board[move[0]][move[1]]
                    board[move[0]][move[1]] = piece
                    board[r][c] = None
                    check = is_check(currentPlayer)

                    #undo the move
                    board[r][c] = piece
                    board[move[0]][move[1]] = temp

                    if not check:
                        return False
    return True

# 41 : 44
#function to handle mouse clicks
def handle_click(pos):
    global selectedPiece, selectedPos, currentPlayer
    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

    if selectedPiece is None:
        piece = board[row][col]
        if piece and piece.color == currentPlayer:
            selectedPiece = piece
            selectedPos = (row,col)

    else:
        if(row, col) in get_valid_moves(selectedPiece, selectedPos[0], selectedPos[1]):

            #move the piece
            board[row][col] = selectedPiece
            board[selectedPos[0]][selectedPos[1]] = None

            #check for pawn promotion
            if selectedPiece.type == 'pawn' and (row == 0 or row == 7):
                board[row][col] = ChessPiece(selectedPiece.color, 'queen', f'images/{selectedPiece.color}_queen.png')

            #switch turns
            currentPlayer = 'black' if currentPlayer == 'white' else 'white'

            #check for game over
            if is_game_over():
                if is_check(currentPlayer):
                    print(f"Checkmate! {currentPlayer.capitalize()} loses.")
                else:
                    print("Stalemate!")
        selectedPiece = None
        selectedPos = None

#main game loop
def main():
    init_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())
        draw_board()
        draw_piece()
        pygame.display.flip()

if __name__ == "__main__":
    main()



        
