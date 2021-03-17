import chess
import math


def MinMax(board, depth, color, alpha=-math.inf, beta=math.inf):
    if depth == 0 or abs(calculate_move(board)) >= abs(10000):
        return None, calculate_move(board)
    moves = chess.getMoves(board, color)
    best_move = None

    if color == chess.Color.black:
        best_score = -math.inf
        for from_move in moves:
            if moves[from_move]:
                for to_move in moves[from_move]:
                    if not chess.isCheck(chess.movePiece(from_move, to_move, board), color):
                        temp_board = chess.movePiece(from_move, to_move, board)
                        score = MinMax(temp_board, depth-1, change_color(color), alpha, beta)[1]
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
                        if best_score == score:
                            best_move = (from_move, to_move)
        return best_move, best_score
    else:
        lowest_score = math.inf
        for from_move in moves:
            if moves[from_move]:
                for to_move in moves[from_move]:
                    temp_board = chess.movePiece(from_move, to_move, board)
                    score = MinMax(temp_board, depth-1, change_color(color), alpha, beta)[1]
                    lowest_score = min(lowest_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
                    else:
                        best_move = (from_move, to_move)
        return best_move, lowest_score


def find_move(board, color):
    depth = get_depth(board)
    move, score = MinMax(board, 3, color)
    return move


def calculate_move(board):
    score = 0
    pieces = get_pieces(board)
    for piece in pieces:
        if chess.isWhite(chess.getColor(piece)):
            multiply = -1
        else:
            multiply = 1

        if chess.isPawn(piece):
            score += multiply * 10
        elif chess.isKnight(piece) or chess.isBishop(piece):
            score += multiply * 30
        elif chess.isRook(piece):
            score += multiply * 50
        elif chess.isQueen(piece):
            score += multiply * 90
        elif chess.isKing(piece):
            score += multiply * 1000
    return score


def get_moves(board, color):
    moves = {}
    for piece in range(64):
        if chess.getColor(chess.getPiece(piece, board)) == color and chess.getPiece(piece, board):
            moves[piece] = chess.isValid(piece, board)
    return moves

def get_depth(board):
    len_pieces = len(get_pieces(board))
    if len_pieces > 15:
        depth = 3
    elif len_pieces > 10:
        depth = 4
    elif len_pieces > 7:
        depth = 5
    elif len_pieces > 5:
        depth = 6
    elif len_pieces > 4:
        depth = 7
    else:
        depth = 8
    return depth


def get_pieces(board):
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
