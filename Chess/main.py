import pygame, sys, random
import chess
import bot

pygame.mixer.pre_init(frequency=44100, size=32, channels=1, buffer=1024)
pygame.init()

place_sound = pygame.mixer.Sound("sounds/place.wav")
place_sound.set_volume(0.025)

window_size = 800


display = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()

background_surface = pygame.transform.scale(pygame.image.load("assets/chessboard.png").convert(), (window_size, window_size))
white_pawn_surface = pygame.transform.scale(pygame.image.load("assets/white_pawn.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
white_rook_surface = pygame.transform.scale(pygame.image.load("assets/white_rook.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
white_knight_surface = pygame.transform.scale(pygame.image.load("assets/white_knight.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
white_bishop_surface = pygame.transform.scale(pygame.image.load("assets/white_bishop.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
white_queen_surface = pygame.transform.scale(pygame.image.load("assets/white_queen.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
white_king_surface = pygame.transform.scale(pygame.image.load("assets/white_king.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_pawn_surface = pygame.transform.scale(pygame.image.load("assets/black_pawn.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_rook_surface = pygame.transform.scale(pygame.image.load("assets/black_rook.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_knight_surface = pygame.transform.scale(pygame.image.load("assets/black_knight.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_bishop_surface = pygame.transform.scale(pygame.image.load("assets/black_bishop.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_queen_surface = pygame.transform.scale(pygame.image.load("assets/black_queen.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))
black_king_surface = pygame.transform.scale(pygame.image.load("assets/black_king.png").convert_alpha(), (int(0.117*window_size), int(0.117*window_size)))


class Chess:
    def __init__(self, window_size):
        self.window_size = window_size

        self.starting_board = 822600792108962701109752665142821874674704896976585017661690405272942910148120593644329604648004
        # self.starting_board = 934518772647114197112938351362149484002244967819837885914675392910601678180483530194841010962432
        self.board = self.starting_board
        self.board_squares = []
        self.board_pieces = []
        self.attacking_squares = []
        self.piece_from = None
        self.piece_from_color = None
        self.piece_to = None
        self.turn = chess.Color.white

        self.game_status = True
        self.bot = True
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
        x_axis = 0.037 * window_size
        y_axis = -0.0175 * window_size
        for y, row in enumerate(self.board_pieces):
            for x, piece in enumerate(row):
                if chess.isWhite(piece):
                    if chess.isPawn(piece):
                        display.blit(white_pawn_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isRook(piece):
                        display.blit(white_rook_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isKnight(piece):
                        display.blit(white_knight_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isBishop(piece):
                        display.blit(white_bishop_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isQueen(piece):
                        display.blit(white_queen_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isKing(piece):
                        display.blit(white_king_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                elif not chess.isWhite(piece):
                    if chess.isPawn(piece):
                        display.blit(black_pawn_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isRook(piece):
                        display.blit(black_rook_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isKnight(piece):
                        display.blit(black_knight_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isBishop(piece):
                        display.blit(black_bishop_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isQueen(piece):
                        display.blit(black_queen_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))
                    elif chess.isKing(piece):
                        display.blit(black_king_surface, (0.12*window_size*x+x_axis, 0.118*window_size*y-y_axis))

    def create_highlights(self):
        y_axis = 0.842*window_size
        for y in range(8):
            x_axis = 0.03548 * window_size
            for x in range(8):
                self.board_squares.append(pygame.Rect(x_axis+2, y_axis+2, int(0.11*window_size), int(0.11*window_size)))
                x_axis += 0.12*window_size
            y_axis -= 0.118*window_size


    def draw_highlights(self, list):
        for x in list:
            pygame.draw.rect(display, (255, 0, 0), self.board_squares[x], 2)

    def check_click_collision(self, mouse_rect):
        old_board = self.board
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
                if old_board == self.board:
                    return
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
        place_sound.play()
        if self.turn == chess.Color.white:
            self.turn = chess.Color.black
        else:
            self.turn = chess.Color.white

    def play_bot(self):
        if self.bot:
            if self.turn == chess.Color.black:
                move = (bot.find_move(self.board, chess.Color.black))
                if move == None:
                    self.game_status = False
                    return
                print(move[0], move[1])
                old_board = self.board
                self.board = chess.movePiece(move[0], move[1], self.board)
                if old_board == self.board:
                    move = chess.getRandomMove(self.board, chess.Color.black)
                    if move:
                        self.board = chess.movePiece(move[0], move[1], self.board)
                    else:
                        self.game_status = False
                        return
                self.create_board_pieces()
                self.attacking_squares = []
                self.piece_from = None
                self.piece_to = None
                self.change_turn()
                return


    def play_game(self):
        while True:
            if self.game_status:
                mouse = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(mouse[0]-1, mouse[1]-1, 1, 1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.check_click_collision(mouse_rect)

            self.blit()
            pygame.time.Clock().tick(60)
            pygame.display.update()
            self.play_bot()


if __name__ == '__main__':
    game = Chess(window_size)

