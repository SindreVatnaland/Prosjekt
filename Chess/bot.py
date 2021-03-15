import chess
from time import sleep

points = 0
opponent_points = 0
move_from = None
move_to = None
opponent_first_move_from = None
opponent_first_move_to = None
opponent_color = None
first_move_from = None
first_move_to = None
bot_color = None
start_depth = 3


def find_move(board, color):
    global move_from
    global move_to
    global start_depth
    global points
    points = -99999
    move_from = None
    move_to = None
    generation(board, start_depth, color)

    return move_from, move_to


def generation(board, k, color):
    global points
    global start_depth
    global move_from
    global move_to
    global opponent_first_move_from
    global opponent_first_move_to
    global first_move_from
    global first_move_to
    if k > 0:
        moves = get_moves(board, color)
        for from_ in moves:
            if not moves[from_] is None:
                for move in moves[from_]:
                    if start_depth == k:
                        first_move_from = from_
                        first_move_to = move
                    elif start_depth - 1:
                        opponent_first_move_from = from_
                        opponent_first_move_to = move
                    generation(chess.movePiece(from_, move, board), k-1, color)
    else:
        if calculate_move(board, color) >= points:
            points = calculate_move(board, color)
            print(points)
            move_from = first_move_from
            move_to = first_move_to



def calculate_move(board, color):
    score = 0
    pieces = find_pieces(board)
    for piece in pieces:
        if chess.getColor(piece) == color:
            multiplier = 1
        else:
            multiplier = -1
        if chess.isPawn(piece):
            score += multiplier * 100
        elif chess.isKnight(piece) or chess.isBishop(piece):
            score += multiplier * 300
        elif chess.isRook(piece):
            score += multiplier * 500
        elif chess.isQueen(piece):
            score += multiplier * 800
        elif chess.isKing(piece):
            score += multiplier * 10000
    return score


def calculate_move_last(board):
    #check if king is in check
    pass

def get_moves(board, color):
    moves = {}
    for piece in range(64):
        if chess.getColor(chess.getPiece(piece, board)) == color:
            moves[piece] = chess.isValid(piece, board)
    return moves

def find_pieces(board):
    pieces = []
    for i in range(64):
        piece = chess.getPiece(i, board)
        if piece:
            pieces.append(piece)
    return pieces

def change_color(color):
    if color == chess.Color.white:
        color = chess.Color.black
    else:
        color = chess.Color.white
    return color
