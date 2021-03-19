import chess
import math
import numpy as np
import random

endgame_value_king = [0, 1, 2, 3, 3, 2, 1, 0,
                      1, 3, 4, 5, 5, 4, 3, 1,
                      2, 4, 6, 7, 7, 6, 4, 2,
                      3, 5, 7, 8, 8, 7, 5, 3,
                      3, 5, 7, 8, 8, 7, 5, 3,
                      2, 4, 6, 7, 7, 6, 4, 2,
                      1, 3, 5, 4, 4, 5, 3, 1,
                      0, 1, 2, 3, 3, 2, 1, 0]


midgame_value = [0, 1, 1, 1, 1, 1, 1, 0,
                 0, 1, 1, 2, 2, 1, 1, 0,
                 1, 1, 2, 3, 3, 2, 1, 1,
                 1, 1, 2, 3, 3, 2, 1, 1,
                 1, 1, 2, 3, 3, 2, 1, 1,
                 1, 1, 2, 3, 3, 2, 1, 1,
                 0, 1, 1, 2, 2, 1, 1, 0,
                 0, 1, 1, 1, 1, 1, 1, 0]

earlygame_value = [0, 1, 1, 1, 1, 1, 1, 0,
                   0, 1, 2, 2, 2, 2, 1, 0,
                   0, 1, 3, 4, 4, 3, 1, 0,
                   0, 1, 4, 5, 5, 4, 1, 0,
                   0, 1, 4, 5, 5, 4, 1, 0,
                   0, 1, 3, 4, 4, 3, 1, 0,
                   0, 1, 2, 2, 2, 2, 1, 0,
                   0, 1, 1, 1, 1, 1, 1, 0]

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
    openings = np.load('openings.npy', allow_pickle='TRUE').item()
    try:
        moves = openings[board]
        move = random.choice(moves)
    except:
        depth = get_depth(board)
        move, score = MinMax(board, depth, color)
    return move


def calculate_move(board):
    score = 0
    pieces = get_pieces(board)
    for piece in pieces:
        if chess.isWhite(piece[0]):
            color = chess.Color.white
            multiplier = -1
            king = 1000
        else:
            color = chess.Color.black
            multiplier = 1
            king = 1200

        if len(pieces) > 10:
            if chess.isPawn(piece[0]):
                score += multiplier * 10
            elif chess.isKnight(piece[0]) or chess.isBishop(piece[0]):
                score += multiplier * 30
            elif chess.isRook(piece[0]):
                score += multiplier * 50
            elif chess.isQueen(piece[0]):
                score += multiplier * 90
            elif chess.isKing(piece[0]):
                score += multiplier * king
        else:
            if chess.isPawn(piece[0]):
                score += multiplier * 2
            elif chess.isKnight(piece[0]) or chess.isBishop(piece[0]):
                score += multiplier * 6
            elif chess.isRook(piece[0]):
                score += multiplier * 9
            elif chess.isQueen(piece[0]):
                score += multiplier * 12
            elif chess.isKing(piece[0]):
                score += multiplier * king

        if len(pieces) > 26:
            if not chess.isKing(piece[1]):
                score += earlygame_value[piece[1]]

        elif len(pieces) > 10:
            if not chess.isKing(piece[1]):
                score += midgame_value[piece[1]]

        # Reward kings on keeping center in endgame **
        elif chess.isKing(piece[0]):
            if chess.isCheck(board, color):
                score -= 50
            weight = -20//(len(pieces)/32)
            score += weight * endgame_value_king[piece[1]]
            score += distance_between_kings(board)

        # Evaluate attacking squares on last depth calculation

        # Evaluate position of every type of piece mid-game

    # print(score)
    return score

def distance_between_kings(board):
    king1 = 0
    for i in range(64):
        if chess.isKing(chess.getPiece(i, board)):
            if king1:
                x = abs(i % 8 - king1 % 8)
                y = abs(i//8 - king1//8)
                value = int(math.sqrt(x**2+y**2))
                return 16 - value
            else:
                king1 = i
    return 16


def get_depth(board):
    len_pieces = len(get_pieces(board))
    if len_pieces > 10:
        depth = 3
    else:
        depth = 4

    return depth


def get_pieces(board):
    pieces = []
    for i in range(64):
        piece = chess.getPiece(i, board)
        if piece:
            pieces.append((piece, i))
    return pieces

def change_color(color):
    if color == chess.Color.white:
        color = chess.Color.black
    else:
        color = chess.Color.white
    return color
