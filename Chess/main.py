import pygame, sys, random
import chess

pygame.mixer.pre_init(frequency = 44100, size = 32, channels = 1, buffer = 1024)
pygame.init()

width = 512
height = 512

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

background_surface = pygame.transform.scale(pygame.image.load("assets/chessboard.png").convert(), (width, height))
white_pawn_surface = pygame.transform.scale(pygame.image.load("assets/white_pawn.png").convert_alpha(), (60, 60))
white_rook_surface = pygame.transform.scale(pygame.image.load("assets/white_rook.png").convert_alpha(), (60, 60))
white_knight_surface = pygame.transform.scale(pygame.image.load("assets/white_knight.png").convert_alpha(), (60, 60))
white_bishop_surface = pygame.transform.scale(pygame.image.load("assets/white_bishop.png").convert_alpha(), (60, 60))
white_queen_surface = pygame.transform.scale(pygame.image.load("assets/white_queen.png").convert_alpha(), (60, 60))
white_king_surface = pygame.transform.scale(pygame.image.load("assets/white_king.png").convert_alpha(), (60, 60))
black_pawn_surface = pygame.transform.scale(pygame.image.load("assets/black_pawn.png").convert_alpha(), (60, 60))
black_rook_surface = pygame.transform.scale(pygame.image.load("assets/black_rook.png").convert_alpha(), (60, 60))
black_knight_surface = pygame.transform.scale(pygame.image.load("assets/black_knight.png").convert_alpha(), (60, 60))
black_bishop_surface = pygame.transform.scale(pygame.image.load("assets/black_bishop.png").convert_alpha(), (60, 60))
black_queen_surface = pygame.transform.scale(pygame.image.load("assets/black_queen.png").convert_alpha(), (60, 60))
black_king_surface = pygame.transform.scale(pygame.image.load("assets/black_king.png").convert_alpha(), (60, 60))


PIPESPAWN = pygame.USEREVENT
pygame.time.set_timer(PIPESPAWN, 1550)


class Chess:
    def __init__(self):
        self.starting_board = 822600792108962701109752665142821874674704896976585017661690405272942910148120593644329604648004
        self.board = self.starting_board
        self.board_squares = []
        self.board_pieces = []
        self.attacking_squares = []
        self.piece_from = None
        self.piece_from_color = None
        self.piece_to = None
        self.turn = chess.Color.white

        self.game_status = True
        self.create_highlights()
        self.create_board_pieces()
        self.play_game()

    def blit(self):
        display.blit(background_surface, (0, 0))
        self.draw_highlights(self.attacking_squares)
        self.draw_board_pieces()

    def create_board_pieces(self):
        self.board_pieces = chess.generateBoard(self.board)

    def draw_board_pieces(self):
        x_axis = 19
        y_axis = -9
        for y, row in enumerate(self.board_pieces):
            for x, piece in enumerate(row):
                if chess.isWhite(piece):
                    if chess.isPawn(piece):
                        display.blit(white_pawn_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isRook(piece):
                        display.blit(white_rook_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isKnight(piece):
                        display.blit(white_knight_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isBishop(piece):
                        display.blit(white_bishop_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isQueen(piece):
                        display.blit(white_queen_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isKing(piece):
                        display.blit(white_king_surface, (61*x+x_axis, 60.3*y-y_axis))
                elif not chess.isWhite(piece):
                    if chess.isPawn(piece):
                        display.blit(black_pawn_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isRook(piece):
                        display.blit(black_rook_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isKnight(piece):
                        display.blit(black_knight_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isBishop(piece):
                        display.blit(black_bishop_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isQueen(piece):
                        display.blit(black_queen_surface, (61*x+x_axis, 60.3*y-y_axis))
                    elif chess.isKing(piece):
                        display.blit(black_king_surface, (61*x+x_axis, 60.3*y-y_axis))

    def create_highlights(self):
        y_axis = 430
        for y in range(8):
            x_axis = 19
            for x in range(8):
                self.board_squares.append(pygame.Rect(x_axis+2, y_axis+2, 56, 56))
                x_axis += 61
            y_axis -= 60.3


    def draw_highlights(self, list):
        for x in list:
            pygame.draw.rect(display, (255, 0, 0), self.board_squares[x], 2)

    def check_click_collision(self, mouse_rect):
        for square, piece in enumerate(self.board_squares):
            if chess.getPiece(square, self.board) and mouse_rect.colliderect(piece) and self.piece_from is None and chess.getColor(chess.getPiece(square, self.board)) == self.turn:
                self.piece_from = square
                self.attacking_squares = chess.isValid(square, self.board)
                return
            elif mouse_rect.colliderect(piece) and square in self.attacking_squares:
                self.piece_to = square
                self.board = chess.movePiece(self.piece_from, self.piece_to, self.board)
                self.create_board_pieces()
                self.attacking_squares = []
                self.piece_from = None
                self.piece_to = None
                self.change_turn()
                return
            elif mouse_rect.colliderect(piece) and not square in self.attacking_squares:
                self.attacking_squares = []
                self.piece_from = None
                self.piece_to = None
                return

    def change_turn(self):
        self.attacking_squares = []
        self.piece_from = None
        self.piece_to = None
        if self.turn == chess.Color.white:
            self.turn = chess.Color.black
        else:
            self.turn = chess.Color.white

    def play_game(self):
        while True:
            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse[0]-1, mouse[1]-1, 1, 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_click_collision(mouse_rect)
            if self.game_status:
                self.blit()


            pygame.time.Clock().tick(30)
            pygame.display.update()





if __name__ == '__main__':
    game = Chess()

